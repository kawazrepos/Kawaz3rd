import json
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from kawaz.core.personas.models import Persona
from kawaz.apps.blogs.tests.factories import EntryFactory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Star
from .factories import StarFactory

def _response_to_dict(response):
    json_string = response.content.decode(encoding='UTF-8')
    obj = json.loads(json_string)
    return obj


class StarListAPITestCase(TestCase):
    def setUp(self):
        self.entry = EntryFactory()
        self.protectedEntry = EntryFactory(pub_state='protected')
        self.user = PersonaFactory()
        self.star0 = StarFactory()
        self.star1 = StarFactory(content_object=self.entry)
        self.star2 = StarFactory(content_object=self.protectedEntry)

    def test_anonymous_get_star_list_via_api(self):
        '''
        Tests anonymous user can get star list of viewable stars via API
        '''
        r = self.client.get('/api/v1/star/')
        obj = _response_to_dict(r)
        self.assertIsNotNone(obj)
        self.assertEqual(len(obj['objects']), 2)

    def test_authorized_get_star_list_via_api(self):
        '''
        Tests authorized user can get all star list via API
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/api/v1/star/')
        obj = _response_to_dict(r)
        self.assertIsNotNone(obj)
        self.assertEqual(len(obj['objects']), 3)

    def test_anonymous_get_star_list_via_api_with_object(self):
        '''
        Tests anonymous user can get star list of specific object via API
        '''
        ct = ContentType.objects.get_for_model(self.entry)
        r = self.client.get('/api/v1/star/?content_type={}&object_id={}'.format(ct.pk, self.entry.pk))
        obj = _response_to_dict(r)
        self.assertIsNotNone(obj)
        self.assertEqual(len(obj['objects']), 1)

class StarCreateAPITestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')

    def test_anonymous_can_not_create_star_via_api(self):
        '''
        Tests anonymous users attempt to create stars via api, then it returns 401 unauthorized.
        '''
        ct = ContentType.objects.get_for_model(Persona)
        data = json.dumps({'content_type' : ct.pk, 'object_id' : 1})
        r = self.client.post('/api/v1/star/', data=data, content_type='application/json')
        self.assertEqual(r.status_code, 401)

    def test_wille_can_not_create_star_via_api(self):
        '''
        Tests wille users attempt to create stars via api, then it returns 401 unauthorized.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        ct = ContentType.objects.get_for_model(Persona)
        data = json.dumps({'content_type' : ct.pk, 'object_id' : 1})
        r = self.client.post('/api/v1/star/', data=data, content_type='application/json')
        self.assertEqual(r.status_code, 401)

    def test_authorized_can_create_star_via_api(self):
        '''
        Tests authorized users can create stars via api
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        ct = ContentType.objects.get_for_model(Persona)
        data = json.dumps({'content_type' : ct.pk, 'object_id' : 1})
        self.assertEqual(Star.objects.count(), 0)
        r = self.client.post('/api/v1/star/', data=data, content_type='application/json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Star.objects.count(), 1)

class StarDeleteAPITestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.other = PersonaFactory()
        self.star = StarFactory(content_object=self.user, author=self.user)
        self.entry = EntryFactory()

    def test_other_can_not_delete_star_via_api(self):
        '''
        Tests other users attempt to delete a star via api, then it returns 401 unauthorized.
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        ct = ContentType.objects.get_for_model(Persona)
        r = self.client.delete('/api/v1/star/1/', content_type='application/json')
        self.assertEqual(r.status_code, 401)
        self.assertEqual(Star.objects.count(), 1)

    def test_owner_can_delete_star_via_api(self):
        '''
        Tests owner can delete their own star via API.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        ct = ContentType.objects.get_for_model(Persona)
        r = self.client.delete('/api/v1/star/1/', content_type='application/json')
        self.assertEqual(r.status_code, 204)
        self.assertEqual(Star.objects.count(), 0)

    def test_content_object_author_can_delete_star_via_api(self):
        '''
        Tests users who owns content object can also delete the star
        '''
        self.assertTrue(self.client.login(username=self.entry.author, password='password'))
        ct = ContentType.objects.get_for_model(Persona)
        self.entryStar = StarFactory(content_object=self.entry)
        r = self.client.delete('/api/v1/star/2/', content_type='application/json')
        self.assertEqual(r.status_code, 204)
        self.assertEqual(Star.objects.count(), 1)
