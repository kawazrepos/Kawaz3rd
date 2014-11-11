# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from .models import ActivitiesTestModelA as ModelA
from .models import ActivitiesTestModelB as ModelB
from .models import ActivitiesTestModelC as ModelC
from ..models import Activity


class ActivitiesModelsActivityManagerTestCase(TestCase):
    def setUp(self):
        self.models = (
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelB.objects.create(text='b'),
            ModelB.objects.create(text='b'),
            ModelC.objects.create(text='c'),
        )
        self.activities = []
        for i, model in enumerate(self.models):
            ct = ContentType.objects.get_for_model(model)
            pk = model.pk
            self.activities.extend([
                Activity.objects.create(content_type=ct,
                                        object_id=pk,
                                        status='created'),
                Activity.objects.create(content_type=ct,
                                        object_id=pk,
                                        status='updated'),
                Activity.objects.create(content_type=ct,
                                        object_id=pk,
                                        status='deleted'),
            ])

    def test_all(self):
        qs = Activity.objects.all()
        ex = map(repr, reversed(self.activities))
        self.assertQuerysetEqual(qs, ex)

    def test_latests(self):
        latests = Activity.objects.latests()
        # the status of latest activity should be 'deleted'
        for latest in latests:
            self.assertEqual(latest.status, 'deleted')

    def test_get_for_model(self):
        qs = Activity.objects.get_for_model(ModelA)
        ex = map(repr, reversed(self.activities[0:9]))
        self.assertQuerysetEqual(qs, ex)

    def test_get_for_object(self):
        qs = Activity.objects.get_for_object(self.models[0])
        ex = map(repr, reversed(self.activities[0:3]))
        self.assertQuerysetEqual(qs, ex)

class ActivitiesModelsActivityTestCase(TestCase):
    def setUp(self):
        self.models = (
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelB.objects.create(text='b'),
            ModelB.objects.create(text='b'),
            ModelC.objects.create(text='c'),
        )

    def test_attributes(self):
        activity = Activity()
        self.assertTrue(hasattr(activity, 'status'))
        self.assertTrue(hasattr(activity, 'remarks'))
        self.assertTrue(hasattr(activity, 'object_id'))
        self.assertTrue(hasattr(activity, 'created_at'))
        self.assertTrue(hasattr(activity, '_snapshot'))
        self.assertTrue(hasattr(activity, 'snapshot'))

    def test_snapshot(self):
        model = self.models[0]
        ct = ContentType.objects.get_for_model(model)
        pk = model.pk
        activity = Activity.objects.create(content_type=ct,
                                           object_id=pk,
                                           status='created')
        activity.snapshot = model
        activity.save()

        loaded_activity = Activity.objects.get(pk=activity.pk)
        self.assertEqual(loaded_activity.snapshot, model)

    def test_get_related_activities(self):
        model1 = self.models[0]
        model2 = self.models[1]
        ct1 = ContentType.objects.get_for_model(model1)
        ct2 = ContentType.objects.get_for_model(model2)
        pk1 = model1.pk
        pk2 = model2.pk
        activity1 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='created')
        activity2 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='updated')
        activity3 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='updated')
        activity4 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='update')
        activity5 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='update')
        activity6 = Activity.objects.create(content_type=ct2,
                                            object_id=pk2,
                                            status='update')
        activities = activity3.get_related_activities()
        self.assertEqual(len(activities), 4)
        # the order of appearance is also important
        self.assertQuerysetEqual(activities,
                                 (5, 4, 2, 1),
                                 transform=lambda x: x.pk)

    def test_previous(self):
        model1 = self.models[0]
        model2 = self.models[1]
        ct1 = ContentType.objects.get_for_model(model1)
        ct2 = ContentType.objects.get_for_model(model2)
        pk1 = model1.pk
        pk2 = model2.pk
        activity1 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='created')
        activity2 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='updated')
        activity3 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='updated')
        activity4 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='update')
        activity5 = Activity.objects.create(content_type=ct1,
                                            object_id=pk1,
                                            status='update')
        activity6 = Activity.objects.create(content_type=ct2,
                                            object_id=pk2,
                                            status='update')
        self.assertEqual(activity1.previous, None)
        self.assertEqual(activity2.previous, activity1)
        self.assertEqual(activity3.previous, activity2)
        self.assertEqual(activity4.previous, activity3)
        self.assertEqual(activity5.previous, activity4)
        self.assertEqual(activity6.previous, None)
