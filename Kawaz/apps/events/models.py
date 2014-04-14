from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..markitupfield.models import MarkItUpField

import datetime

class EventManager(models.Manager):
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
        else:
            return self.none()

class Event(models.Model):
    """
    The model which indicates events
    """

    PUB_STATES = (
        ('public',      _("Public")),
        ('protected',   _("Internal")),
        ('draft',       _("Draft")),
    )
    # Required
    pub_state = models.CharField(_("Publish status"), max_length=10, choices=PUB_STATES, default="public")
    title = models.CharField(_("Title"), max_length=255)
    # body = MarkItUpField(_("Body"), default_markup_type="markdown")
    # Unrequired
    period_start = models.DateTimeField(_("Start time"), blank=True, null=True)
    period_end = models.DateTimeField(_("End time"), blank=True, null=True)
    place = models.CharField(_("Place"), max_length=255, blank=True)
    # Uneditable
    organizer = models.ForeignKey(User, verbose_name=_("Organizer"), related_name="events_owned", editable=False)
    attendees = models.ManyToManyField(User, verbose_name=_("Attendees"), related_name="events_attend", null=True, editable=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified at"), auto_now=True)

    gcal            = models.URLField(verbose_name="GCalEditLink", blank=True, null=True, editable=False)
    
    objects         = EventManager()
    
    class Meta:
        ordering            = ('period_start', 'period_end', '-created_at', '-updated_at', 'title')
        verbose_name        = _("Event")
        verbose_name_plural = _("Events")

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
        super(Event, self).clean()
        
    def attend(self, user, save=True):
        '''Add user to attendee'''
        self.attendees.add(user)
        if save:
            self.save()

    def quit(self, user, save=True):
        '''Remove user from attendee'''
        if user == self.organizer:
            raise AttributeError("Organizer doesn't allow to quit the event.")
        if not user in self.attendees.all():
            raise AttributeError("Username %s have not be attendee of this event")
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

@receiver(post_save, sender=Event)
def join_organizer(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        instance.attend(instance.organizer)