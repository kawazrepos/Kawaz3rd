from unittest.mock import MagicMock
from django.template import Context
from django.template.loader import render_to_string
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
        return r

    def test_can_show_authenticated_index_by_authenticated_user(self):
        """
        ログインユーザーが/にアクセスして、マイページを見れるかどうか
        """
        r = self._test_template("/", 'index.authenticated', True)
        request = MagicMock()
        request.path = '/'
        c = Context({
            'request': request,
            'user': self.authenticated_user
        })
        rendered = render_to_string('components/registration/index.authenticated.html', c)
        self.assertEqual(r.content.decode('utf-8').strip(), rendered.strip())

    def test_can_show_authenticated_index_by_authenticated_user_with_external(self):
        """
        ログインユーザーが/?external=1にアクセスして、外部ユーザー向けトップを見れるかどうか
        """
        r = self._test_template("/?external=1", 'index.authenticated', True)
        request = MagicMock()
        request.path = '/?external=1'
        c = Context({
            'request': request
        })
        rendered = render_to_string('components/registration/index.anonymous.html', c)
        self.assertEqual(r.content.decode('utf-8').strip(), rendered.strip())

    def test_access_to_about(self):
        """
        /about/にアクセスして、roughpages/about.htmlが表示できるかどうか
        """
        self._test_template("/about/")

    def test_access_to_contact(self):
        """
        /contact/にアクセスして、roughpages/contact.htmlが表示できるかどうか
        """
        self._test_template("/contact/")

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

    def test_access_to_registration(self):
        """
        /registration/にアクセスして、roughpages/registration.htmlが表示できるかどうか
        """
        self._test_template("/registration/")

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

    def test_access_to_drafts_with_authenticated(self):
        """
        /draftsにアクセスして、roughpages/drafts.authenticated.htmlが表示できるかどうか
        """
        self._test_template("/drafts/", "drafts.authenticated", authenticated=True)

    def test_access_to_helps(self):
        """
        /helpsにアクセスして、roughpages/helps.htmlが表示できるかどうか
        """
        self._test_template("/helps/", "helps")

    def test_access_to_helps(self):
        """
        /helpsにアクセスして、roughpages/helps.htmlが表示できるかどうか
        """
        self._test_template("/helps/", "helps")

    def test_access_to_helps_event(self):
        """
        /helps/events/にアクセスして、roughpages/helps/events.htmlが表示できるかどうか
        """
        self._test_template("/helps/events/", "helps/events")

    def test_access_to_helps_markdown(self):
        """
        /helps/markdown/にアクセスして、roughpages/helps/markdown.htmlが表示できるかどうか
        """
        self._test_template("/helps/markdown/", "helps/markdown")

    def test_access_to_helps_products(self):
        """
        /helps/products/にアクセスして、roughpages/helps/products.htmlが表示できるかどうか
        """
        self._test_template("/helps/products/", "helps/products")

    def test_access_to_helps(self):
        """
        /helps/profiles/にアクセスして、roughpages/helps/profiles.htmlが表示できるかどうか
        """
        self._test_template("/helps/profiles/", "helps/profiles")

    def test_access_to_helps_projects(self):
        """
        /helps/projects/にアクセスして、roughpages/helps/projects.htmlが表示できるかどうか
        """
        self._test_template("/helps/projects/", "helps/projects")

    def test_access_to_helps_welcome(self):
        """
        /helps/welcome/にアクセスして、roughpages/helps/welcome.htmlが表示できるかどうか
        """
        self._test_template("/helps/welcome/", "helps/welcome")

    def test_access_to_guideline_credits(self):
        """
        /guideline/credits/にアクセスして、roughpages/guideline/credits.htmlが表示できるかどうか
        """
        self._test_template("/guideline/credits/", "guideline/credits")