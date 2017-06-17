# coding=utf-8
"""
"""

import os
from django.test import TestCase
from unittest.mock import MagicMock, patch, PropertyMock
from ..conf import settings
from ..client import (require_enabled,
                      GoogleCalendarClient)


class GoogleCalendarClientRequireEnabledDecoratorTestCase(TestCase):
    def test_require_enabled_call_method(self):
        """
        decorated method should be called if `enabled` is True
        """
        method = MagicMock(return_value=True)
        decorated = require_enabled(method)
        # Mock to behave as the first argument of class method
        _self = MagicMock()
        _self.enabled = True
        self.assertTrue(decorated(_self))
        self.assertTrue(method.called)

    def test_require_enabled_do_not_call_method(self):
        """
        decorated method should not be called if `enabled` is False
        """
        method = MagicMock(return_value=True)
        decorated = require_enabled(method)
        # Mock to behave as the first argument of class method
        _self = MagicMock()
        _self.enabled = False
        self.assertIsNone(decorated(_self))
        self.assertFalse(method.called)


class GoogleCalendarClientTestCaseBase(TestCase):
    @patch('google_calendar.models.GoogleCalendarBridge')
    def setUp(self, GoogleCalendarBridge):
        self.event = {
            'id': 1000,
            'summary': 'Appointment',
            'location': 'Somewhere',
            'start': {
                'dateTime': '2014-12-03T10:00:00.000-07:00'
            },
            'end': {
                'dateTime': '2014-12-03T10:25:00.000-07:00'
            },
        }
        self.bridge = MagicMock()
        GoogleCalendarBridge.objects.get_or_create.return_value = [
            self.bridge
        ]
        self.client = GoogleCalendarClient(
            settings.GOOGLE_CALENDAR_CALENDAR_ID
        )


if os.path.exists(settings.GOOGLE_CALENDAR_CREDENTIALS):
    @patch.object(
        GoogleCalendarClient,
        '_client',
        new_callable=PropertyMock
    )
    class GoogleCalendarClientTestCase(GoogleCalendarClientTestCaseBase):

        def test_insert(self, *args):
            resource = MagicMock()
            resource.execute.return_value = self.event
            self.client._client.insert.return_value = resource
            event = self.client.insert(self.event)

            self.assertIsNotNone(event)
            self.assertEqual(event['summary'], 'Appointment')
            self.client._client.insert.assert_called_with(
                calendarId=self.client.calendar_id,
                body=self.event)

        def test_patch(self, *args):
            resource = MagicMock()
            self.client._client.patch.return_value = resource
            patched_event = dict(self.event)
            patched_event['summary'] = 'foobar'
            resource.execute.return_value = patched_event

            event = self.client.patch(
                patched_event['id'],
                {'summary': 'foobar'})
            self.assertEqual(event['summary'], 'foobar')
            self.client._client.patch.assert_called_with(
                calendarId=self.client.calendar_id,
                eventId=patched_event['id'],
                body={'summary': 'foobar'})

        def test_delete(self, *args):
            event = dict(self.event)
            resource = MagicMock()
            self.client._client.delete.return_value = resource
            self.client.delete(event['id'])

            self.assertEqual(self.client._client.delete.called, 1)
            self.client._client.delete.assert_called_with(
                calendarId=self.client.calendar_id,
                eventId=self.event['id'])
else:
    class GoogleCalendarClientTestCase(GoogleCalendarClientTestCaseBase):
        def setUp(self):
            # disable warnings
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                super().setUp()

        def test_insert(self):
            self.assertIsNone(self.client.insert(self.event))

        def test_patch(self):
            self.assertIsNone(self.client.patch('0', self.event))

        def test_delete(self):
            self.assertIsNone(self.client.delete('0'))
