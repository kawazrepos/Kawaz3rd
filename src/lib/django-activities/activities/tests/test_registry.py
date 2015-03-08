# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.db.models import Model
from unittest.mock import MagicMock
from ..models import Activity
from ..mediator import ActivityMediator
from ..registry import Registry


class ActivitiesRegistryTestCase(TestCase):
    def test_register(self):
        registry = Registry()

        model = MagicMock(spec=Model)()
        model._meta.concrete_model._meta.app_label = 'activities'
        model._meta.concrete_model._meta.model_name = 'mock'
        mediator = MagicMock(spec=ActivityMediator)

        registry.register(model, mediator)
        # mediator should be connected to model via 'connect' method
        mediator.connect.assert_called_with(model)
        # model and mediator should be connected in registry as well
        self.assertEqual(registry.get(model), mediator)

    def test_register_default(self):
        registry = Registry()

        model = MagicMock(spec=Model)()
        model._meta.concrete_model._meta.app_label = 'activities'
        model._meta.concrete_model._meta.model_name = 'mock'

        registry.register(model)
        mediator = registry.get(model)
        self.assertEqual(mediator.__class__, ActivityMediator)

    def test_get(self):
        registry = Registry()
        model = MagicMock(spec=Model)()
        model._meta.concrete_model._meta.app_label = 'activities'
        model._meta.concrete_model._meta.model_name = 'mock'
        mediator = MagicMock(spec=ActivityMediator)

        registry.register(model, mediator)

        activity = MagicMock(spec=Activity)
        activity.content_type.model_class.return_value = model

        self.assertEqual(registry.get(activity), mediator)
