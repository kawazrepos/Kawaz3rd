import datetime
from django.conf import settings
from django.db import models
from django.db.models import Q, F, Count
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from kawaz.core.db.decorators import validate_on_save
from kawaz.core.publishments.models import PUB_STATES
from kawaz.core.publishments.models import PublishmentManagerMixin


class Category(models.Model):
    """
    イベントの大カテゴリ
    運営が設置したものをユーザーが選ぶ
    """
    label = models.CharField(_('Label'), max_length=16, unique=True)
    order = models.PositiveSmallIntegerField(_('Order'))

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('order'),
        verbose_name = _('Label')
        verbose_name_plural = _('Label')


class EventManager(models.Manager, PublishmentManagerMixin):
    author_field_name = 'organizer'

    def active(self, user):
        """
        指定されたユーザーに公開されたイベントの中で、まだ終わっていない
        or イベントの終了時期が指定されていないイベントを含むクエリを返す
        """
        qs = self.published(user)
        qs = qs.filter(Q(period_end__gte=timezone.now()) |
                       Q(period_end=None))
        return qs

    def attendable(self, user):
        """
        指定されたユーザーに公開されたイベントの中で、参加可能なイベントを
        含むクエリを返す
        """
        qs = self.active(user)
        # 締め切りによるフィルタリング
        q1 = (Q(attendance_deadline__gte=timezone.now()) |
              Q(attendance_deadline=None))
        # 参加人数によるフィルタリング
        q2 = (Q(number_restriction__gt=F('attendees_count')) |
              Q(number_restriction=None))
        return qs.annotate(attendees_count=Count('attendees')).filter(q1 & q2)


@validate_on_save
class Event(models.Model):
    # 必須フィールド
    pub_state = models.CharField(_("Publish status"),
                                 max_length=10, choices=PUB_STATES,
                                 default="public")
    title = models.CharField(_("Title"), max_length=255)
    body = models.TextField(_("Body"))

    # 省略可能フィールド
    period_start = models.DateTimeField(_("Start time"),
                                        blank=True, null=True)
    period_end = models.DateTimeField(_("End time"),
                                      blank=True, null=True)
    place = models.CharField(_("Place"), max_length=255, blank=True)
    number_restriction = models.PositiveIntegerField(
        _('Number restriction'),
        default=None, blank=True, null=True,
        help_text=_("Use this to limit the number of attendees."))
    attendance_deadline = models.DateTimeField(
        _('Attendance deadline'),
        default=None, blank=True, null=True,
        help_text=_("A deadline of the attendance. "
                    "No member can attend the event after this deadline."))
    # 編集不可フィールド
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name=_("Organizer"),
                                  related_name="events_owned",
                                  editable=False)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       verbose_name=_("Attendees"),
                                       related_name="events_attend",
                                       editable=False)
    category = models.ForeignKey(Category, verbose_name=_('Category'), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified at"), auto_now=True)
    gcal_id = models.CharField(_("Calendar ID"), default='', editable=False, max_length=128)

    objects = EventManager()

    class Meta:
        ordering = (
            'period_start', 'period_end',
            '-created_at', '-updated_at',
            'title', '-pk')
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        permissions = (
            ('attend_event', 'Can attend the event'),
            ('quit_event', 'Can quit the event'),
            ('view_event', 'Can view the event'),
        )

    def __str__(self):
        return self.title

    def clean(self):
        """
        下記のルールに従ってValidationする
        1.  イベント終了時間は開始時間より遅い必要がある（時間は逆行できない）
        2.  過去のイベントは作成できない（スネーク！タイムパラドックスだ！）
        3.  ７日以上にまたがるイベントは作成できない
        4.  開始時間が指定されているが終了時間が指定されていないイベントは
            作成できない（一生イベントに参加とかは物理的に不可能）
        5.  参加者制限が0人のイベントは作成できない
        6.  参加締め切りは未来でなければいけない
        """
        if self.period_start and self.period_end:
            if self.period_start > self.period_end:
                raise ValidationError(
                    _('End time must be later than start time.'))
            elif (self.period_start < timezone.now() and
                  (not self.pk or
                   Event.objects.filter(pk=self.pk).count() == 0)):
                raise ValidationError(_('Start time must be future.'))
            elif (self.period_end - self.period_start).days > 7:
                raise ValidationError(_('The period of event is too long.'))
        elif self.period_end and not self.period_start:
            raise ValidationError(_('You must set end time too'))
        if self.number_restriction is not None and self.number_restriction < 1:
            raise ValidationError(
                _("Number restriction should be grater than 0"))
        if (self.attendance_deadline and
                self.attendance_deadline < timezone.now() and
            (not self.pk or
                Event.objects.filter(pk=self.pk).count() == 0)):
            raise ValidationError(_('Attendance deadline must be future.'))

    def attend(self, user, save=True):
        """指定されたユーザーをこのイベントに参加させる"""
        if not user.has_perm('events.attend_event', obj=self):
            raise PermissionDenied
        self.attendees.add(user)
        if save:
            self.save()

    def quit(self, user, save=True):
        """指定されたユーザーをこのイベントから退会させる"""
        if not user.has_perm('events.quit_event', obj=self):
            raise PermissionDenied
        self.attendees.remove(user)
        if save:
            self.save()

    def is_attendee(self, user):
        """参加者か否か"""
        return user in self.attendees.all()

    def is_active(self):
        """イベントが終了していないか否か"""
        if not self.period_start:
            return True
        return self.period_end >= timezone.now()

    def is_over_restriction(self):
        """人数制限を超えているか否か"""
        if not self.number_restriction:
            return False
        return self.attendees.count() >= self.number_restriction

    def is_over_deadline(self):
        """参加締め切りを超えているか否か"""
        if not self.attendance_deadline:
            return False
        return self.attendance_deadline <= timezone.now()

    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('events_event_update', (), {'pk': self.pk})
        return ('events_event_detail', (), {'pk': self.pk})


from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Event)
def join_organizer(**kwargs):
    """
    作成者を自動的に参加させるシグナルレシーバ
    """
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        instance.attend(instance.organizer)


from permission import add_permission_logic
from .perms import EventPermissionLogic
from kawaz.core.publishments.perms import PublishmentPermissionLogic
add_permission_logic(Event, EventPermissionLogic()),
add_permission_logic(Event, PublishmentPermissionLogic(
    author_field_name='organizer')),

from .utils.gcal import GoogleCalendarUpdater
@receiver(post_save, sender=Event)
def update_gcal(sender, instance, created, **kwargs):
    """
    イベント作成、更新時にGoogleカレンダーと同期するシグナルレシーバー
    """
    updater = GoogleCalendarUpdater()
    updater.update_event(instance, created)


@receiver(post_delete, sender=Event)
def delete_gcal(sender, instance, **kwargs):
    """
    イベント削除時に、Googleカレンダーから削除するシグナルレシーバー
    """
    updater = GoogleCalendarUpdater()
    updater.delete_event(instance)
