# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.test.utils import override_settings
from unittest.mock import MagicMock, patch
from ..backend import (tolerate, Backend, get_backend_class, get_backend)


class GoogleCalendarBackendTolerateTestCase(TestCase):
    @override_settings(DEBUG=True)
    def test_tolerate_disabled_v1(self):
        def fn():
            raise Exception
        decorated = tolerate(fn)
        self.assertRaises(Exception, decorated)

    @override_settings(DEBUG=False)
    def test_tolerate_disabled_v2(self):
        def fn():
            raise Exception
        decorated = tolerate(fn)
        self.assertRaises(Exception, decorated, fail_silently=False)

    @override_settings(DEBUG=False)
    def test_tolerate_enabled(self):
        def fn():
            raise Exception
        decorated = tolerate(fn)
        decorated()


class GoogleCalendarBackendTestCase(TestCase):
    def setUp(self):
        patcher1 = patch('google_calendar.backend.GoogleCalendarClient')
        patcher2 = patch('google_calendar.models.GoogleCalendarBridge')
        self.GoogleCalendarClient = patcher1.start()
        self.GoogleCalendarBridge = patcher2.start()
        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)

        self.event = MagicMock()
        self.bridge = MagicMock()
        self.GoogleCalendarBridge.objects.get_or_create.return_value = [
            self.bridge
        ]
        self.backend = Backend()

    def test_get_bridge(self):
        self.assertEqual(self.bridge,
                         self.backend.get_bridge(self.event))

    def test_translate(self):
        self.assertRaises(NotImplementedError,
                          self.backend.translate, self.event)

    def test_is_valid(self):
        self.assertTrue(self.backend.is_valid(self.event))

    def test_update_create(self):
        self.bridge.gcal_event_id = None
        self.backend.translate = MagicMock()
        self.backend.update(self.event, fail_silently=False)
        self.assertTrue(self.backend.client.insert.called)
        self.assertTrue(self.bridge.save.called)

    def test_update_update(self):
        self.bridge.gcal_event_id = 100
        self.backend.translate = MagicMock()
        self.backend.update(self.event, fail_silently=False)
        self.assertTrue(self.backend.client.patch.called)
        self.assertFalse(self.bridge.save.called)

    def test_update_delete(self):
        self.bridge.gcal_event_id = 100
        self.backend.is_valid = MagicMock(return_value=False)
        self.backend.translate = MagicMock()
        self.backend.update(self.event, fail_silently=False)
        self.assertTrue(self.backend.client.delete.called)
        self.assertTrue(self.bridge.delete.called)

    def test_delete_success(self):
        self.bridge.gcal_event_id = 100
        self.backend.delete(self.event, fail_silently=False)
        self.assertTrue(self.backend.client.delete.called)
        self.assertTrue(self.bridge.delete.called)

    def test_delete_fail(self):
        self.bridge.gcal_event_id = None
        self.backend.delete(self.event, fail_silently=False)
        self.assertFalse(self.backend.client.delete.called)
        self.assertFalse(self.bridge.delete.called)


class GoogleCalendarBackendFunctionsTestCase(TestCase):
    def test_get_backend_class(self):
        cls = get_backend_class()
        self.assertIsNotNone(cls)

    def test_get_backend(self):
        # it should be singleton
        cls = get_backend_class()
        b1 = get_backend()
        b2 = get_backend()
        self.assertTrue(isinstance(b1, cls))
        self.assertTrue(isinstance(b2, cls))
        self.assertEqual(b1, b2)
