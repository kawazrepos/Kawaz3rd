from django.test import TestCase

from kawaz.core.personas.tests.factories import PersonaFactory


class KawazIndexViewTestCase(TestCase):
    def test_anonymous_user(self):
        """
        非ログインユーザーはAnonymousIndexにリダイレクトされます
        """
        response = self.client.get("")
        self.assertTemplateUsed(response, 'core/anonymous_index.html')

    def test_authorized_user(self):
        """
        ログインユーザーはAuthorizedIndexにリダイレクトされます
        """
        user = PersonaFactory()

        self.assertTrue(self.client.login(username=user.username,
                                          password='password'))
        response = self.client.get("")
        self.assertTemplateUsed(response, 'core/authenticated_index.html')
