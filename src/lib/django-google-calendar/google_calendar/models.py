# coding=utf-8
"""
"""

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.core.exceptions import ImproperlyConfigured

from .conf import settings
from .utils import resolve_relation_lazy
from .backend import get_backend

DISPATCH_UID = 'gcal_google_calendar_bridge'


# Check if the required variable was specified
if not settings.GOOGLE_CALENDAR_EVENT_MODEL:
    raise ImproperlyConfigured(
        "GOOGLE_CALENDAR_EVENT_MODEL is required to be specified"
    )


class GoogleCalendarBridge(models.Model):
    """
    A bridge model which enable Google Calendar Sync with Event like model
    """
    event = models.OneToOneField(settings.GOOGLE_CALENDAR_EVENT_MODEL,
                                 primary_key=True)
    gcal_event_id = models.CharField(_("Google Calendar Event ID"),
                                     default='', editable=False,
                                     blank=True, max_length=128)


def update_google_calendar(sender, instance, created, **kwargs):
    # Ignore when events models are created by fixtures.
    if kwargs.get('raw', False):
        return
    backend = get_backend()
    send_notifications = getattr(settings, 'GOOGLE_CALENDER_ENABLE_NOTIFICATIONS', False)
    backend.update(instance, sendNotifications=send_notifications)


def delete_google_calendar(sender, instance, **kwargs):
    backend = get_backend()
    backend.delete(instance)


def register_signals(sender, **kwargs):
    post_save.connect(update_google_calendar, sender=sender)
    pre_delete.connect(delete_google_calendar, sender=sender)
resolve_relation_lazy(settings.GOOGLE_CALENDAR_EVENT_MODEL, register_signals)
