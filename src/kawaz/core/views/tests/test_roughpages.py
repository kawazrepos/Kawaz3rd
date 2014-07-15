from django.test import TestCase
from kawaz.core.personas.tests.factories import PersonaFactory


class KawazRoughPageTestCase(TestCase):
    def setUp(self):
        self.authenticated_user = PersonaFactory()

    def _test_template(self, url, filename=None, authenticated=False):
        if authenticated:
            self.assertTrue(self.client.login(
                username=self.authenticated_user.username,
                password='password'
            ))
        filename = filename or url.replace("/", "")
        r = self.client.get(url)
        self.assertTemplateUsed(r, "roughpages/{}.html".format(filename))

    def test_access_to_about(self):
        """
        /about/にアクセスして、roughpages/about.htmlが表示できるかどうか
        """
        self._test_template("/about/")

    def test_access_to_published(self):
        """
        /published/にアクセスして、roughpages/published.htmlが表示できるかどうか
        """
        self._test_template("/published/")

    def test_access_to_rules(self):
        """
        /rules/にアクセスして、roughpages/rules.htmlが表示できるかどうか
        """
        self._test_template("/rules/")

    def test_access_to_index_with_anonymous(self):
        """
        /にアクセスして、roughpages/index.anonymous.htmlが表示できるかどうか
        """
        self._test_template("/", "index.anonymous")

    def test_access_to_index_with_authenticated(self):
        """
        /にアクセスして、roughpages/index.authenticated.htmlが表示できるかどうか
        """
        self._test_template("/", "index.authenticated", authenticated=True)
