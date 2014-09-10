# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from unittest.mock import MagicMock
from ..utils import (get_model,
                     get_class)


class GCalUtilsGetModelTestCase(TestCase):
    def test_get_model_with_str(self):
        from ..models import GoogleCalendarBridge
        path = 'gcal.GoogleCalendarBridge'
        model = get_model(path)
        self.assertEqual(model, GoogleCalendarBridge)

    def test_get_model_with_cls(self):
        from ..models import GoogleCalendarBridge
        model = get_model(GoogleCalendarBridge)
        self.assertEqual(model, GoogleCalendarBridge)

    def test_get_model_with_unknown(self):
        """get_model should return None if the path doesn't exists"""
        path = 'gcal.UnknownModel'
        model = get_model(path)
        self.assertEqual(model, None)


class GCalUtilsGetClassTestCase(TestCase):
    def test_get_class_with_str(self):
        from ..client import GoogleCalendarClient
        path = 'kawaz.core.gcal.client.GoogleCalendarClient'
        cls = get_class(path)
        self.assertEqual(cls, GoogleCalendarClient)

    def test_get_class_with_cls(self):
        from ..client import GoogleCalendarClient
        cls = get_class(GoogleCalendarClient)
        self.assertEqual(cls, GoogleCalendarClient)

    def test_get_class_with_unknown_module(self):
        from django.core.exceptions import ImproperlyConfigured
        path = 'kawaz.core.gcal.unknown.GoogleCalendarClient'
        self.assertRaises(ImproperlyConfigured, get_class, path)

    def test_get_class_with_unknown_class(self):
        from django.core.exceptions import ImproperlyConfigured
        path = 'kawaz.core.gcal.client.Unknown'
        self.assertRaises(ImproperlyConfigured, get_class, path)


