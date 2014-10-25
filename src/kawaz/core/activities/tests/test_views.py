from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from activities.registry import registry
from activities.mediator import ActivityMediator
from .models import KawazActivitiesTestModelA, KawazActivitiesTestModelB
from kawaz.core.activities.tests.factories import ActivityFactory

__author__ = 'giginet'

class ActivityViewTestCase(TestCase):

    def setUp(self):
        registry.register(KawazActivitiesTestModelA, ActivityMediator())
        registry.register(KawazActivitiesTestModelB, ActivityMediator())

    def test_activities_activity_list_url(self):
        """
        name=activities_activity_listから/activities/を引ける
        """
        self.assertEqual(reverse('activities_activity_list'), '/activities/')

    def test_get_activities(self):
        """
        10件ずつActivityを取得できる
        """
        for i in range(15):
            model = KawazActivitiesTestModelA.objects.create(text="aaa")
        r = self.client.get('/activities/')
        self.assertEqual(len(r.context['object_list']), 10)

        r = self.client.get('/activities/?page=2')
        self.assertEqual(len(r.context['object_list']), 10)
        self.assertIsNotNone(r.context['page_obj'])
        self.assertIsNotNone(r.context['paginator'])

    def test_get_latest_activities(self):
        """
         type=wallのとき、latestsの物だけを10件取得できる
        """
        model0 = KawazActivitiesTestModelA.objects.create(text="aaa")
        model1 = KawazActivitiesTestModelB.objects.create(text="aaa")

        r = self.client.get('/activities/?type=wall')
        self.assertEqual(len(r.context['object_list']), 2)

        r = self.client.get('/activities/')
        self.assertEqual(len(r.context['object_list']), 6)
