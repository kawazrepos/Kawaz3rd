from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import RegistrationProfileFactory

class RegistrationViewTestCase(TestCase):
    def test_can_display_register_view(self):
        """
        /registration/register/が表示できるか
        """
        r = self.client.get("/registration/register/")
        self.assertTemplateUsed(r, "registration/registration_form.html")

    def test_registration_supplement(self):
        """
        /registration/register/のフォームに追加フォームが表示されているかどうか
        """
        r = self.client.get("/registration/register/")
        form = r.context['supplement_form']
        self.assertEqual(len(form.fields), 3)
        self.assertTrue('skill' in form.fields)
        self.assertTrue('place' in form.fields)
        self.assertTrue('remarks' in form.fields)

    def test_redirect_to_registration_complete(self):
        """
        registration完了後に/registration/register/complete/に遷移するかどうか
        """
        r = self.client.post("/registration/register/", {
            'username' : 'kawaztan',
            'email1' : 'webmaster@kawaz.org',
            'email2' : 'webmaster@kawaz.org',
            'place' : '安息の地',
            'skill' : 'マスコットできます！'
        })
        self.assertRedirects(r, '/registration/register/complete/')

    def test_can_display_registration_complete(self):
        """
        /registration/register/complete/が表示できるか
        """
        r = self.client.get("/registration/register/complete/")
        self.assertTemplateUsed(r, 'registration/registration_complete.html')

    @override_settings(
        REGISTRATION_OPEN=False
    )
    def test_redirect_registration_closed(self):
        """
        新規会員登録停止時に`registration_closed`に遷移するかどうか
        """
        r = self.client.get("/registration/register/")
        self.assertRedirects(r, '/registration/register/closed/')

    def test_can_display_registration_closed(self):
        """
        /registration/register/closed/が表示できるか
        """
        r = self.client.get("/registration/register/closed/")
        self.assertTemplateUsed(r, "registration/registration_closed.html")

class ActivationViewTestCase(TestCase):
    def test_can_display_activate_complete(self):
        """
        /registration/activate/complete/が表示できるか
        """
        r = self.client.get("/registration/activate/complete/")
        self.assertTemplateUsed(r, "registration/activation_complete.html")

    def test_can_display_activate(self):
        """
        /registration/activate/<activation_key>が表示できるか
        """
        RegistrationProfileFactory(activation_key="hello", _status='accepted')
        r = self.client.get("/registration/activate/hello/")
        self.assertTemplateUsed(r, "registration/activation_form.html")


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()

    def _assert_authenticated(self, neg=False):
        if neg:
            self.assertNotIn('_auth_user_id', self.client.session)
        else:
            self.assertIn('_auth_user_id', self.client.session)

    def test_can_reverse_logout(self):
        """
        name=loginからURLを引ける
        """
        url = reverse('logout')
        self.assertEqual(url, '/registration/logout/')

    def test_can_logout_via_post(self):
        """
        LogoutページにPOSTしたとき、ログアウトできる
        """
        self.assertTrue(self.client.login(username=self.user.username, password='password'))
        self._assert_authenticated()
        r = self.client.post('/registration/logout/')
        self._assert_authenticated(neg=True)

    def test_can_not_logout_via_get(self):
        """
        LogoutページにGETしたとき、ログアウトできない
        """
        self.assertTrue(self.client.login(username=self.user.username, password='password'))
        self._assert_authenticated()
        r = self.client.get('/registration/logout/')
        self._assert_authenticated()

    def test_can_view_logout_page(self):
        """
        LogoutページにGETしたとき、ログアウトページが見れる
        """
        self.assertTrue(self.client.login(username=self.user.username, password='password'))
        r = self.client.get('/registration/logout/')
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'registration/logout.html')

