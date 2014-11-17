from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from activities.models import Activity
from activities.tests.models import ActivitiesTestModelA
from activities.registry import registry
from activities.mediator import ActivityMediator
from kawaz.core.personas.models import Persona
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.activities.tests.factories import ActivityFactory

__author__ = 'giginet'

registry.register(ActivitiesTestModelA, ActivityMediator())

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
        ct = ContentType.objects.get_for_model(ActivitiesTestModelA)
        for i in range(15):
            test_model = ActivitiesTestModelA(text="hogehoge")
            test_model.save()

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
        for i in range(15):
            # 作成する
            test_model = ActivitiesTestModelA(text="hogehoge")
            test_model.save()
            # 更新する
            test_model.nickname = 'hoge'
            test_model.save()
        # 1つのinstanceあたり2つ、合計30個のActivityが生成されてるはず

        r = self.client.get('/activities/?type=wall')
        self.assertEqual(len(r.context['object_list']), 10)
        r = self.client.get('/activities/?type=wall&page=2')
        self.assertEqual(len(r.context['object_list']), 5)

        r = self.client.get('/activities/')
        self.assertEqual(len(r.context['object_list']), 10)
        r = self.client.get('/activities/?page=2')
        self.assertEqual(len(r.context['object_list']), 10)
        r = self.client.get('/activities/?page=3')
        self.assertEqual(len(r.context['object_list']), 10)
