from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from kawaz.core.personas.models import Persona
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import RegistrationProfileFactory


class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='user')

    def _test_can_display(self, relative_url, template_name):
        url = "/registration/{}/".format(relative_url)
        template = "registration/{}.html".format(template_name)
        r = self.client.get(url)
        self.assertTemplateUsed(r, template)

    def _test_url_name(self, name, url):
        self.assertEqual(reverse(name), url)

    def _assert_authenticated(self, neg=False):
        if neg:
            self.assertNotIn('_auth_user_id', self.client.session)
        else:
            self.assertIn('_auth_user_id', self.client.session)

    def test_can_reverse_logout(self):
        """
        reverse('logout') からLogout用URLを引ける
        """
        url = reverse('logout')
        self.assertEqual(url, '/registration/logout/')

    def test_can_display_login_view(self):
        """
        /registration/login/が表示できるか
        """
        self._test_url_name('login', '/registration/login/')
        self._test_can_display('login', 'login')

    def test_can_logout_via_post(self):
        """
        LogoutページにPOSTしたとき、ログアウトして、トップページに行く
        """
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self._assert_authenticated()
        r = self.client.post('/registration/logout/')
        self._assert_authenticated(neg=True)
        self.assertRedirects(r, '/')

    def test_can_not_logout_via_get(self):
        """
        LogoutページにGETしたとき、ログアウトして、トップページに行く
        """
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self._assert_authenticated()
        r = self.client.get('/registration/logout/')
        self._assert_authenticated(neg=True)
        self.assertRedirects(r, '/')


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

    def test_can_display_activate(self):
        """
        /registration/activate/<activation_key>が表示できるか
        """
        RegistrationProfileFactory(activation_key="hello", _status='accepted')
        r = self.client.get("/registration/activate/hello/")
        self.assertTemplateUsed(r, "registration/activation_form.html")

    def test_can_display_activate_complete(self):
        """
        /registration/activate/complete/が表示できるか
        """
        r = self.client.get("/registration/activate/complete/")
        self.assertTemplateUsed(r, "registration/activation_complete.html")

    def test_can_display_password_change_view(self):
        """
        ログインユーザーが/registration/password_change/が表示できるか
        """
        self.client.login(username='user', password='password')
        self._test_url_name('password_change',
                            '/registration/password_change/')
        self._test_can_display('password_change', 'password_change_form')

    def test_can_display_password_change_done_view(self):
        """
        ログインユーザーが/registration/password_change/done/が表示できるか
        """
        self.client.login(username='user', password='password')
        self._test_url_name('password_change_done',
                            '/registration/password_change/done/')
        self._test_can_display('password_change/done', 'password_change_done')

    def test_can_display_password_reset_view(self):
        """
        /registration/password_reset/が表示できるか
        """
        self._test_url_name('password_reset', '/registration/password_reset/')
        self._test_can_display('password_reset', 'password_reset_form')

    def test_can_display_password_reset_complete_view(self):
        """
        /registration/reset/done/が表示できるか
        """
        self._test_url_name('password_reset_complete',
                            '/registration/reset/done/')
        self._test_can_display('reset/done',
                               'password_reset_complete')

    def test_can_display_password_reset_done_view(self):
        """
        /registration/password/reset/done/が表示できるか
        """
        self._test_url_name('password_reset_done',
                            '/registration/password_reset/done/')
        self._test_can_display('password_reset/done', 'password_reset_done')


class ParticipantsApplicationViewTestCase(TestCase):
    def test_create_user_after_application(self):
        """
        登録フォームからユーザー登録をしたとき、ユーザーが生成される
        """
        before_count = Persona.objects.count()
        self.assertEqual(Persona.objects.count(), before_count + 1)
        r = self.client.post("/registration/register/", {
            'username' : 'kawaztan',
            'email1' : 'webmaster@kawaz.org',
            'email2' : 'webmaster@kawaz.org',
            'place' : '安息の地',
            'skill' : 'マスコットできます！'
        })

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

    def test_can_display_activate(self):
        """
        /registration/activate/<activation_key>が表示できるか
        """
        RegistrationProfileFactory(activation_key="hello", _status='accepted')
        r = self.client.get("/registration/activate/hello/")
        self.assertTemplateUsed(r, "registration/activation_form.html")

    def test_can_display_activate_complete(self):
        """
        /registration/activate/complete/が表示できるか
        """
        r = self.client.get("/registration/activate/complete/")
        self.assertTemplateUsed(r, "registration/activation_complete.html")

    def test_can_display_password_change_view(self):
        """
        ログインユーザーが/registration/password_change/が表示できるか
        """
        self.client.login(username='user', password='password')
        self._test_url_name('password_change',
                            '/registration/password_change/')
        self._test_can_display('password_change', 'password_change_form')

    def test_can_display_password_change_done_view(self):
        """
        ログインユーザーが/registration/password_change/done/が表示できるか
        """
        self.client.login(username='user', password='password')
        self._test_url_name('password_change_done',
                            '/registration/password_change/done/')
        self._test_can_display('password_change/done', 'password_change_done')

    def test_can_display_password_reset_view(self):
        """
        /registration/password_reset/が表示できるか
        """
        self._test_url_name('password_reset', '/registration/password_reset/')
        self._test_can_display('password_reset', 'password_reset_form')

    def test_can_display_password_reset_complete_view(self):
        """
        /registration/reset/done/が表示できるか
        """
        self._test_url_name('password_reset_complete',
                            '/registration/reset/done/')
        self._test_can_display('reset/done',
                               'password_reset_complete')

    def test_can_display_password_reset_done_view(self):
        """
        /registration/password/reset/done/が表示できるか
        """
        self._test_url_name('password_reset_done',
                            '/registration/password_reset/done/')
        self._test_can_display('password_reset/done', 'password_reset_done')


class ParticipantsApplicationViewTestCase(TestCase):
    def test_create_user_after_application(self):
        """
        登録フォームからユーザー登録をしたとき、ユーザーが生成される
        """
        before_count = Persona.objects.count()
        r = self.client.post("/registration/register/", {
            'username' : 'kawaztan',
            'email1' : 'webmaster@kawaz.org',
            'email2' : 'webmaster@kawaz.org',
            'place' : '安息の地',
            'skill' : 'マスコットできます！'
        })
        self.assertEqual(Persona.objects.count(), before_count + 1)
        self.assertRedirects(r, '/registration/register/complete/')
        self.assertIsNotNone(Persona.objects.get(username='kawaztan'))

    def test_new_user_should_be_wille(self):
        """
        登録フォームから登録したユーザーがwille権限になる
        アクティベーションした瞬間にchildrenになる
        """
        r = self.client.post("/registration/register/", {
            'username' : 'kawaztan',
            'email1' : 'webmaster@kawaz.org',
            'email2' : 'webmaster@kawaz.org',
            'place' : '安息の地',
            'skill' : 'マスコットできます！'
        })
        new_user = Persona.objects.get(username='kawaztan')
        self.assertEqual(new_user.role, 'wille')
