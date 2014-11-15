# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from unittest.mock import MagicMock
from ...notifiers.base import ActivityNotifierBase
from ...notifiers.registry import Registry


class ActivitiesNotifierRegistryTestCase(TestCase):
    def test_register(self):
        registry = Registry()

        notifier = MagicMock(spec=ActivityNotifierBase)
        name = repr(notifier.__class__)

        # without name specification
        registry.register(notifier)
        self.assertTrue(name in registry)
        self.assertEqual(registry.get(name), notifier)

        # with name specification
        name = MagicMock()
        registry.register(notifier, name)
        self.assertTrue(name in registry)
        self.assertEqual(registry.get(name), notifier)

    def test_register_duplicate(self):
        registry = Registry()

        notifier = MagicMock(spec=ActivityNotifierBase)
        name = repr(notifier.__class__)
        registry.register(notifier)

        self.assertRaises(AttributeError,
                          registry.register,
                          notifier)

    def test_get_or_register(self):
        registry = Registry()

        notifier = MagicMock(spec=ActivityNotifierBase)
        name = repr(notifier.__class__)

        result1 = registry.get_or_register(notifier)
        self.assertEqual(result1, notifier)
        result2 = registry.get_or_register(notifier)
        self.assertEqual(result2, notifier)

    def test_get(self):
        registry = Registry()
        notifier = MagicMock(spec=ActivityNotifierBase)
        name = repr(notifier.__class__)
        registry.register(notifier)

        self.assertEqual(registry.get(name), notifier)
        self.assertEqual(registry.get(notifier), notifier)

    def test__contains__(self):
        registry = Registry()
        notifier = MagicMock(spec=ActivityNotifierBase)
        name = repr(notifier.__class__)
        registry.register(notifier)

        self.assertTrue(name in registry)
        self.assertTrue(notifier in registry)

