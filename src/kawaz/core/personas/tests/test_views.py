from django.test import TestCase
from django.core.urlresolvers import reverse
from kawaz.core.personas.tests.factories import PersonaFactory

class PersonaViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='user')

    def _test_can_display(self, relative_url, template_name):
        url = "/registration/{}/".format(relative_url)
        template = "registration/{}.html".format(template_name)
        r = self.client.get(url)
        self.assertTemplateUsed(r, template)

    def _test_url_name(self, name, url):
        self.assertEqual(reverse(name), url)

    def test_can_display_login_view(self):
        """
        /registration/login/が表示できるか
        """
        self._test_url_name('login', '/registration/login/')
        self._test_can_display('login', 'login')

    def test_can_display_logout_view(self):
        """
        /registration/logout/を表示すると、トップページにリダイレクトするか
        """
        self._test_url_name('logout', '/registration/logout/')
        url = "/registration/logout/"
        r = self.client.get(url)
        self.assertRedirects(r, '/')

    def test_can_display_password_change_view(self):
        """
        ログインユーザーが/registration/password/change/が表示できるか
        """
        self.client.login(username='user', password='password')
        self._test_url_name('password_change', '/registration/password/change/')
        self._test_can_display('password/change', 'password_change_form')

    def test_can_display_password_change_done_view(self):
        """
        ログインユーザーが/registration/password/change/done/が表示できるか
        """
        self.client.login(username='user', password='password')
        self._test_url_name('password_change_done', '/registration/password/change/done/')
        self._test_can_display('password/change/done', 'password_change_done')

    def test_can_display_password_reset_view(self):
        """
        /registration/password/reset/が表示できるか
        """
        self._test_url_name('password_reset', '/registration/password/reset/')
        self._test_can_display('password/reset', 'password_reset_form')

    def test_can_display_password_reset_complete_view(self):
        """
        /registration/password/reset/complete/が表示できるか
        """
        self._test_url_name('password_reset_complete', '/registration/password/reset/complete/')
        self._test_can_display('password/reset/complete', 'password_reset_complete')

    def test_can_display_password_reset_done_view(self):
        """
        /registration/password/reset/done/が表示できるか
        """
        self._test_url_name('password_reset_done', '/registration/password/reset/done/')
        self._test_can_display('password/reset/done', 'password_reset_done')
