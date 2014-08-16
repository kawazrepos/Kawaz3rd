# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import tolerance
from .conf import settings
from .utils import get_class
from .client import GoogleCalendarClient


RFC3339 = '%Y-%m-%dT%H:%M:%S.000%z'


def tolerate(fn):
    """
    A function decorator to make the function fail silently if 
    settings.DEBUG is False or fail_silently=True is specified
    """
    def switch_function(*args, **kwargs):
        fail_silently = kwargs.pop('fail_silently', True)
        if settings.DEBUG or not fail_silently:
            return False, args, kwargs
        return True, args, kwargs
    return tolerance.tolerate(switch=switch_function)(fn)


class Backend(object):
    """
    A manipulation backend between a event like model and a bridge model
    """
    @classmethod
    def strftime(cls, datetime):
        """
        Format datetime object into RFC3339 which Google Calendar API require
        """
        return datetime.strftime(RFC3339)

    @classmethod
    def get_bridge(cls, event):
        """
        Get a bridge instance of the specified event instance
        """
        from .models import GoogleCalendarBridge
        return GoogleCalendarBridge.objects.get_or_create(event=event)[0]

    def __init__(self):
        self.calendar_id = settings.GOOGLE_CALENDAR_ID
        self.client = GoogleCalendarClient(self.calendar_id)

    def translate(self, event):
        """
        Trasnlate an event like object to a body parameter of Google Calendar
        API.

        Subclass must override this method
        """
        raise NotImplementedError

    def is_valid(self, event, raise_exception=False):
        """
        Check if the specified event like object is valid for translating to
        body parameter of Google Calender API

        Subclass should override this method
        """
        return True

    @tolerate
    def update(self, event, **kwargs):
        """
        Update an event on Google Calendar of the specified event instance
        """
        bridge = self.__class__.get_bridge(event)
        if bridge.gcal_event_id:
            # patch or delete event
            if self.is_valid(event):
                self.client.patch(bridge.gcal_event_id,
                                  self.translate(event), **kwargs)
            else:
                self.client.delete(bridge.gcal_event_id)
                bridge.delete()
        elif self.is_valid(event):
            gcal_event_id = self.client.insert(self.translate(event),
                                               **kwargs)
            if gcal_event_id is not None:
                bridge.gcal_event_id = gcal_event_id
                bridge.save()

    @tolerate
    def delete(self, event):
        """
        Delete an event on Google Calendar of the specified event instance
        """
        bridge = self.__class__.get_bridge(event)
        if bridge.event_id:
            self.client.delete(bridge.event_id)
            bridge.delete()


def get_backend_class():
    """
    Get a backend class
    """
    return get_class(settings.GOOGLE_CALENDAR_BACKEND_CLASS)


def get_backend():
    """
    Get a backend instance
    """
    cache_name = '_cached_backend_instance'
    if not hasattr(get_backend, cache_name):
        setattr(get_backend, cache_name, get_backend_class()())
    return getattr(get_backend, cache_name)
