from django.test import TestCase
from kawaz.core.personas.tests.factories import PersonaFactory

class PersonaViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='user')

    def _test_can_reach(self, relative_url, template_name):
        url = "/registration/{}/".format(relative_url)
        template = "registration/{}.html".format(template_name)
        r = self.client.get(url)
        self.assertTemplateUsed(r, template)

    def test_can_reach_login_view(self):
        """
        /registration/login/に到達できるか
        """
        self._test_can_reach('login', 'login')

    def test_can_reach_logout_view(self):
        """
        /registration/logout/に到達できるか
        """
        self._test_can_reach('logout', 'logout')

    def test_can_reach_password_change_view(self):
        """
        ログインユーザーが/registration/password/change/に到達できるか
        """
        self.client.login(username='user', password='password')
        self._test_can_reach('password/change', 'password_change_form')

    def test_can_reach_password_change_done_view(self):
        """
        ログインユーザーが/registration/password/change/done/に到達できるか
        """
        self.client.login(username='user', password='password')
        self._test_can_reach('password/change', 'password_change_done')

    def test_can_reach_password_reset_view(self):
        """
        /registration/password/reset/に到達できるか
        """
        self._test_can_reach('password/reset', 'password_reset_form')

    def test_can_reach_password_reset_complete_view(self):
        """
        /registration/password/reset/complete/に到達できるか
        """
        self._test_can_reach('password/reset/complete', 'password_reset_complete')

    def test_can_reach_password_reset_done_view(self):
        """
        /registration/password/reset/done/に到達できるか
        """
        self._test_can_reach('password/reset/done', 'password_reset_done')
