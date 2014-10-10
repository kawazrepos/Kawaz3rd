# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from unittest.mock import MagicMock
from ..mediator import ActivityMediator
from ..registry import Registry


class ActivitiesRegistryTestCase(TestCase):
    def test_register(self):
        registry = Registry()

        model = MagicMock()
        mediator = MagicMock(spec=ActivityMediator)

        registry.register(model, mediator)
        # mediator should be connected to model via 'connect' method
        mediator.connect.assert_called_with(model)
        # model and mediator should be connected in registry as well
        self.assertEqual(registry._registry[model], mediator)

    def test_register_default(self):
        registry = Registry()

        model = MagicMock()

        registry.register(model)
        mediator = registry._registry[model]
        self.assertEqual(mediator.__class__, ActivityMediator)

    def test_get(self):
        registry = Registry()
        model = MagicMock()
        mediator = MagicMock(spec=ActivityMediator)
        registry.register(model, mediator)

        activity = MagicMock()
        activity.content_object._meta.model = model

        self.assertEqual(registry.get(activity), mediator)
