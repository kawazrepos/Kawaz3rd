# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from django.contrib.contenttypes.models import ContentType
from django.template import Context
from django.test import TestCase
from activities.models import Activity
from activities.registry import registry
from kawaz.core.comments.tests.factories import CommentFactory

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

        self._test_render(activities[0])

    def _test_partial_update(self, context_names = (), **fields):
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

        self._test_render(activities[0])

    def _test_delete(self):
        ct = ContentType.objects.get_for_model(self.object)
        pk = self.object.pk
        self.object.delete()
        activity = Activity.objects.filter(content_type=ct, object_id=pk).first()

        self.assertEqual(activity.status, 'deleted')

        self._test_render(activity)

    def _test_comment_added(self):
        """
        commentしたときに、comment_addedが発行される
        """
        nactivities = Activity.objects.get_for_object(self.object).count()

        # コメントをする
        comment = CommentFactory(content_object=self.object)

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'comment_added')
        self.assertEqual(activity.snapshot, self.object)
        # remarksにコメントのpkが入る
        self.assertEqual(activity.remarks, str(comment.pk))

        self._test_render(activity)
        mediator = registry.get(activity)
        context = mediator.prepare_context(activity, Context())
        self.assertTrue('comment' in context, """context doesn't contain 'comment'""")


    def _test_render(self, activity):
        mediator = registry.get(activity)
        self.assertTrue(mediator.render(activity, Context()))
