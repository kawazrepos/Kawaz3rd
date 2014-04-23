from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied

from django.db.models.signals import post_save
from django.dispatch import receiver

from kawaz.core.db.decorators import validate_on_save
from kawaz.core.permissions.logics import PUB_STATES

from markupfield.fields import MarkupField


import datetime

class EventManager(models.Manager):
    '''ObjectManager for Event model'''

    def active(self, user):
        qs = self.published(user)
        qs = qs.filter(Q(period_end__gte=datetime.datetime.now()) | Q(period_end=None)).distinct()
        return qs
    
    def published(self, user):
        q = Q(pub_state='public')
        if user and user.is_authenticated():
            q |= Q(pub_state='protected')
        return self.filter(q).distinct()
    
    def draft(self, user):
        if user and user.is_authenticated():
            return self.filter(organizer=user, pub_state='draft')
        return self.none()

@validate_on_save
class Event(models.Model):
    """
    The model which indicates events
    """
    # Required
    pub_state = models.CharField(_("Publish status"), max_length=10, choices=PUB_STATES, default="public")
    title = models.CharField(_("Title"), max_length=255)
    body = MarkupField(_("Body"), default_markup_type="markdown")
    # Unrequired
    period_start = models.DateTimeField(_("Start time"), blank=True, null=True)
    period_end = models.DateTimeField(_("End time"), blank=True, null=True)
    place = models.CharField(_("Place"), max_length=255, blank=True)
    # Uneditable
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Organizer"), related_name="events_owned", editable=False)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Attendees"), related_name="events_attend", editable=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified at"), auto_now=True)

    objects = EventManager()
    
    class Meta:
        ordering = ('period_start', 'period_end', '-created_at', '-updated_at', 'title', '-pk')
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
        if self.period_start and self.period_end:
            if self.period_start > self.period_end:
                raise ValidationError(_('End time must be later than start time.'))
            elif self.period_start < datetime.datetime.now() and (not self.pk or Event.objects.filter(pk=self.pk).count() == 0):
                raise ValidationError(_('Start time must be future.'))
            elif (self.period_end - self.period_start).days > 7:
                raise ValidationError(_('The period of event is too long.'))
        elif self.period_end and not self.period_start:
            raise ValidationError(_('You must set end time too'))

    def attend(self, user, save=True):
        '''Add user to attendees'''
        if not user.has_perm('events.attend_event', obj=self):
            raise PermissionDenied
        self.attendees.add(user)
        if save:
            self.save()

    def quit(self, user, save=True):
        '''Remove user from attendees'''
        if not user.has_perm('events.quit_event', obj=self):
            raise PermissionDenied
        self.attendees.remove(user)
        if save:
            self.save()

    def is_attendee(self, user):
        '''Check passed user is whether attendee or not'''
        return user in self.attendees.all()

    def is_active(self):
        '''Return the boolean value which indicates event is active or not'''
        if not self.period_start:
            return True
        return self.period_end >= datetime.datetime.now()

    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('events_event_update', (str(self.pk)))
        return ('events_event_detail', (str(self.pk)))


@receiver(post_save, sender=Event)
def join_organizer(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        instance.attend(instance.organizer)

from permission import add_permission_logic
from .perms import EventPermissionLogic
from .perms import PubStatePermissionLogic
add_permission_logic(Event, EventPermissionLogic()),
add_permission_logic(Event, PubStatePermissionLogic(author_field_name='organizer')),
