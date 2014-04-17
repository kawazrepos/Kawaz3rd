from django.test import TestCase
from django.core.urlresolvers import reverse

from kawaz.core.personas.tests.factories import PersonaFactory

class KawazIndexViewTestCase(TestCase):

    def test_anonymous_user(self):
        '''Tests an anonymous user can view anonymous index'''
        url = reverse('kawaz_index')
        response = self.client.get(url)
        self.assertTemplateUsed(response.template_name, 'core/anonymous_index.html')

    def test_authorized_user(self):
        '''Tests an authorized user can view anonymous index'''
        user = PersonaFactory()
        user.set_password('password')
        user.save()

        url = reverse('kawaz_index')
        self.assertTrue(self.client.login(username=user.username, password='password'))
        response = self.client.get(url)
        self.assertTemplateUsed(response.template_name, 'core/anonymous_index.html')
