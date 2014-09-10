# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.core.exceptions import ImproperlyConfigured
from django.dispatch import receiver

from .conf import settings
from .utils import get_model, resolve_relation_lazy
from .backend import get_backend

DISPATCH_UID = 'gcal_google_calendar_bridge'


# Check if the required variable was specified
if not settings.GCAL_EVENT_MODEL:
    raise ImproperlyConfigured("GCAL_EVENT_MODEL is required to be specified")


class GoogleCalendarBridge(models.Model):
    """
    A bridge model which enable Google Calendar Sync with Event like model
    """
    event = models.OneToOneField(settings.GCAL_EVENT_MODEL,
                                 primary_key=True)
    gcal_event_id = models.CharField(_("Google Calendar Event ID"),
                                     default='', editable=False,
                                     blank=True, max_length=128)


def update_google_calendar(sender, instance, created, **kwargs):
    backend = get_backend()
    backend.update(instance)


def delete_google_calendar(sender, instance, **kwargs):
    backend = get_backend()
    backend.delete(instance)


def register_signals(sender, **kwargs):
    post_save.connect(update_google_calendar, sender=sender)
    pre_delete.connect(delete_google_calendar, sender=sender)
resolve_relation_lazy(settings.GCAL_EVENT_MODEL, register_signals)
