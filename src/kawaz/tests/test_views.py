from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.conf import settings

from kawaz.core.personas.tests.factories import PersonaFactory

class KawazIndexViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')

    def test_anonymous_user(self):
        '''Tests an anonymous user can view anonymous index'''
        c = Client()
        url = reverse('kawaz_index')
        response = c.get(url)
        self.assertListEqual(response.template_name, ['kawaz/anonymous_index.html',])

    def test_authorized_user(self):
        '''Tests an authorized user can view anonymous index'''
        c = Client()
        url = reverse('kawaz_index')
        c.login(username=self.user.username, password='password')
        response = c.get(url)
        self.assertListEqual(response.template_name, ['kawaz/anonymous_index.html'])
