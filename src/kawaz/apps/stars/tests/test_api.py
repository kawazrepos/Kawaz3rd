import json
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from kawaz.core.personas.models import Persona
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Star
from .factories import StarFactory

def _response_to_dict(response):
    json_string = response.content.decode(encoding='UTF-8')
    obj = json.loads(json_string)
    return obj


class StarListAPITestCase(TestCase):
    def setUp(self):
        self.user0 = PersonaFactory()
        self.user1 = PersonaFactory()
        self.star0 = Star.objects.add_to_object(self.user0, self.user0)
        self.star1 = Star.objects.add_to_object(self.user1, self.user0)

    def test_anonymous_get_star_list_via_api(self):
        '''
        Tests anonymous user can get star list of all stars via API
        '''
        r = self.client.get('/api/v1/star/')
        obj = _response_to_dict(r)
        self.assertIsNotNone(obj)
        self.assertEqual(len(obj['objects']), 2)

    def test_anonymous_get_star_list_via_api_with_object(self):
        '''
        Tests anonymous user can get star list of specific object via API
        '''
        ct = ContentType.objects.get_for_model(Persona)
        r = self.client.get('/api/v1/star/?content_type={}&object_id=1'.format(ct.pk))
        obj = _response_to_dict(r)
        self.assertIsNotNone(obj)
        self.assertEqual(len(obj['objects']), 1)

