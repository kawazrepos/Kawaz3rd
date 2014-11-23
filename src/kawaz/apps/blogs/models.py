import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import get_default_timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from activities.registry import registry
from kawaz.core.db.decorators import validate_on_save
from kawaz.core.publishments.models import PUB_STATES
from kawaz.core.publishments.models import PublishmentManagerMixin


class Category(models.Model):
    """
    ブログが所属するカテゴリーモデル

    カテゴリーは各ユーザーがそれぞれ所有するもので、自身のブログの整理に利用する
    目的で存在する。
    """
    label = models.CharField(_('Category name'), max_length=255)
    # TODO Fix Me
    # editable=FalseにしてるとAPIからアクセスできない
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('Author'),
                               related_name='blog_categories')

    class Meta:
        # カテゴリはユーザーが所有するものなので unique together を指定
        unique_together = (('author', 'label'),)

    def __str__(self):
        return "{}({})".format(self.label, self.author.username)

    @models.permalink
    def get_absolute_url(self):
        return ('blogs_entry_category_list', (), {'author': self.author.username, 'pk': self.pk})


class EntryManager(models.Manager, PublishmentManagerMixin):
    pass


@validate_on_save
class Entry(models.Model):
    """
    ブログ記事モデル
    """
    pub_state = models.CharField(_("Publish status"),
                                 max_length=10, choices=PUB_STATES,
                                 default="public")
    title = models.CharField(_('Title'), max_length=255)
    body = models.TextField(_('Body'))
    category = models.ForeignKey(Category, verbose_name=_('Category'),
                                 related_name="entries",
                                 blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('Author'),
                               related_name='blog_entries', editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modified at'), auto_now=True)
    published_at = models.DateTimeField(_('Published at'),
                                      null=True, editable=False)

    objects = EntryManager()

    class Meta:
        ordering = ('-updated_at', 'title')
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        permissions = (
            ('view_entry', 'Can view the entry'),
        )

    def __str__(self):
        return self.title

    @property
    def published_at_date(self):
        """公開日"""
        if not self.published_at:
            return None
        return datetime.datetime.date(self.published_at)

    def save(self, *args, **kwargs):
        if not self.published_at:
            # 記事の状態が下書き以外の場合は公開日時を自動的に指定
            # これは最初の公開時のみに行われるため 公開->下書き->公開 としても
            # 最初の公開日が変更されることはない
            if self.pub_state != 'draft':
                self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def clean(self):
        if self.category and self.author != self.category.author:
            raise ValidationError('Category must be owned by author.')
        super().clean()

    @models.permalink
    def get_absolute_url(self):
        if self.published_at:
            tz = get_default_timezone()
            published_at = self.published_at.astimezone(tz)
            return ('blogs_entry_detail', (), {
                'author': self.author.username,
                'year': published_at.year,
                'month': published_at.month,
                'day': published_at.day,
                'pk': self.pk
            })
        return ('blogs_entry_update', (), {
            'author': self.author.username,
            'pk': self.pk
        })


from permission import add_permission_logic
from kawaz.core.publishments.perms import PublishmentPermissionLogic
from kawaz.core.personas.perms import ChildrenPermissionLogic
from kawaz.core.personas.perms import KawazAuthorPermissionLogic

add_permission_logic(Category, KawazAuthorPermissionLogic(
    field_name='author',
    any_permission=True
))
add_permission_logic(Category, ChildrenPermissionLogic(
    add_permission=True
))

add_permission_logic(Entry, KawazAuthorPermissionLogic(
    field_name='author',
    any_permission=True,
))
add_permission_logic(Entry, PublishmentPermissionLogic())

from .activity import EntryActivityMediator
registry.register(Entry, EntryActivityMediator())
