# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from django.template import Context
from django.test import TestCase
from activities.models import Activity
from activities.registry import registry

__author__ = 'giginet'

class BaseActivityMediatorTestCase(TestCase):
    factory_class = None

    def setUp(self):
        self.object = self.factory_class()

    def _test_create(self):
        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0].status, 'created')
        self.assertEqual(activities[0].snapshot, self.object)

    def _test_partial_update(self, fields, context_names):
        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(len(activities), 1)
        for field, value in fields.items():
            setattr(self.object, field, value)
        self.object.save()

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(len(activities), 2)
        activity = activities[0]
        self.assertEqual(activity.status, 'updated')
        mediator = registry.get(activity)
        context = Context()
        context = mediator.prepare_context(activity, context)
        for name in context_names:
            self.assertTrue(name in context, 'context variable {} is not contained'.format(name))

    def _test_delete(self):
        self.object.delete()
        # 削除されたモデルに対してget_for_objectは使えない
        activity = Activity.objects.all()[1]

        self.assertEqual(activity.status, 'deleted')
