# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from unittest.mock import MagicMock
from ..client import require_enabled


class EventsGCalClientRequireEnabledDecoratorTestCase(TestCase):
    def test_require_enabled_call_method(self):
        """
        decorated method should be called if `enabled` is True
        """
        method = MagicMock(return_value=True)
        decorated = require_enabled(method)
        self = MagicMock()
        self.enabled = True
        self.assertTrue(decorated(self))
        self.assertTrue(method.called)

    def test_require_enabled_do_not_call_method(self):
        """
        decorated method should not be called if `enabled` is False
        """
        method = MagicMock(return_value=True)
        decorated = require_enabled(method)
        self = MagicMock()
        self.enabled = False
        self.assertIsNone(decorated(self))
        self.assertFalse(method.called)
