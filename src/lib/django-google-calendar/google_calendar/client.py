# coding=utf-8
"""
Google Calendar manipulation library (Raw level)
"""

import warnings
import httplib2

# require: google_api_python_client
from apiclient import discovery
from oauth2client.file import Storage

from .conf import settings


class ImproperlyConfiguredWarning(UserWarning):
    """
    A warning class which indicate an improper configur
    """
    pass


def require_enabled(method):
    """
    A method decorator which return None if self.enabled is False, otherwise
    it execute the decorated method and return the result
    """
    def inner(self, *args, **kwargs):
        if not self.enabled:
            return None
        return method(self, *args, **kwargs)
    return inner


class GoogleCalendarClient(object):
    """
    A raw level google calendar API client class
    """
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        storage = Storage(settings.GOOGLE_CALENDAR_CREDENTIALS)
        credentials = storage.get()
        # Login Google API with a credentials
        if credentials is None or credentials.invalid:
            COMMAND_NAME = 'login_to_google_calendar_api'
            warnings.warn((
                'No valid Google API credentials are available. '
                'Execute python manage.py {} and '
                'follow the instructions.'
            ).format(COMMAND_NAME), category=ImproperlyConfiguredWarning)
            self.enabled = False
        else:
            http = credentials.authorize(http=httplib2.Http())
            self.service = discovery.build('calendar', 'v3', http=http)
            self.enabled = True

    @property
    def _client(self):
        return self.service.events()

    @require_enabled
    def get(self, event_id, **kwargs):
        """
        get a google calendar event
        """
        event = self._client.get(calendarId=self.calendar_id,
                                 eventId=event_id,
                                 **kwargs).execute()
        return event

    @require_enabled
    def insert(self, event, **kwargs):
        """
        Insert a google calendar event
        """
        created = self._client.insert(calendarId=self.calendar_id,
                                      body=event,
                                      **kwargs).execute()
        return created

    @require_enabled
    def patch(self, event_id, event, **kwargs):
        """
        Patch the google calendar event specified by event_id
        """
        patched = self._client.patch(calendarId=self.calendar_id,
                                     eventId=event_id,
                                     body=event,
                                     **kwargs).execute()
        return patched

    @require_enabled
    def delete(self, event_id, **kwargs):
        """
        Delete the google calendar event specified by event_id
        """
        self._client.delete(calendarId=self.calendar_id,
                            eventId=event_id,
                            **kwargs).execute()
        return None
