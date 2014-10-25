from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from activities.tests.models import ActivitiesTestModelA, ActivitiesTestModelB, ActivitiesTestModelC
from kawaz.core.activities.tests.factories import ActivityFactory

__author__ = 'giginet'

class ActivityViewTestCase(TestCase):
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
            model = ActivitiesTestModelA(text="aaa")
            model.save()
            ct = ContentType.objects.get_for_model(ActivitiesTestModelA)
            ActivityFactory(content_type=ct, object_id=model.pk)
        r = self.client.get('/activities/')
        self.assertEqual(len(r.context['object_list']), 10)

        r = self.client.get('/activities/?page=2')
        self.assertEqual(len(r.context['object_list']), 5)
        self.assertIsNotNone(r.context['page_obj'])
        self.assertIsNotNone(r.context['paginator'])

    def test_get_latest_activities(self):
        """
         type=wallのとき、latestsの物だけを10件取得できる
        """
        model0 = ActivitiesTestModelA(text="aaa")
        model0.save()
        model1 = ActivitiesTestModelB(text="aaa")
        model1.save()
        ct0 = ContentType.objects.get_for_model(ActivitiesTestModelA)
        ct1 = ContentType.objects.get_for_model(ActivitiesTestModelB)
        for i in range(5):
            ActivityFactory(content_type=ct0, object_id=model0.pk)
            ActivityFactory(content_type=ct1, object_id=model1.pk)

        r = self.client.get('/activities/?type=wall')
        self.assertEqual(len(r.context['object_list']), 2)

        r = self.client.get('/activities/')
        self.assertEqual(len(r.context['object_list']), 10)
