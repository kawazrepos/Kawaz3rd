from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.core.urlresolvers import reverse
from kawaz.apps.profiles.tests.factories import ProfileFactory
from kawaz.core.personas.models import Persona
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


class PersonaUpdateViewTestCase(TestCase):
    def setUp(self):
        self.members = (
                PersonaFactory(role='adam'),
                PersonaFactory(role='seele'),
                PersonaFactory(role='nerv'),
                PersonaFactory(role='children'),
            )
        self.non_members = (
                PersonaFactory(role='wille'),
                AnonymousUser(),
            )
        self.persona_kwargs = {
            'last_name': '井ノ中',
            'first_name': 'かわず',
            'nickname': 'かわずたん',
            'gender': 'woman',
            'quotes': 'けろーん',
            'email': 'kawaztan@kawaz.org',
            'avatar': None
        }

    def prefer_login(self, user):
        if user.is_authenticated():
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))

    def test_can_reverse_persona_update_url(self):
        """
        personas_persona_updateが/registration/update/に割り当てられている
        """
        self.assertEqual(reverse('personas_persona_update'), '/registration/update/')


    def test_non_members_cannot_see_persona_update_view(self):
        """
        非メンバーはユーザー編集ページは見ることが出来ない
        """
        login_url = settings.LOGIN_URL+'?next=/registration/update/'
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get('/registration/update/')
            self.assertRedirects(r, login_url)

    def test_member_can_get_oneself(self):
        """
        メンバーがユーザー編集ページにアクセスしたとき、自分のオブジェクトが返ってくる
        """
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get('/registration/update/')
            self.assertEqual(r.context['object'], user,
                             '{} must not able to see persona update view.'.format(user.username))

    def test_non_members_cannot_update_persona(self):
        """
        非メンバーはユーザー情報を編集できない
        """
        login_url = settings.LOGIN_URL+'?next=/registration/update/'
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.post('/registration/update/', self.persona_kwargs)
            self.assertRedirects(r, login_url)

    def test_members_can_update_own_persona(self):
        """
        メンバーは自分のユーザー情報を編集できる
        """
        persona_count = Persona.objects.count()
        for user in self.members:
            self.prefer_login(user)
            profile = ProfileFactory(user=user)
            r = self.client.post('/registration/update/', self.persona_kwargs)
            self.assertRedirects(r, '/members/{}/'.format(user.username))
            self.assertEqual(Persona.objects.count(), persona_count)
            self.assertTrue('messages' in r.cookies, "No messages are appeared")
            u = Persona.objects.get(pk=user.pk)
            self.assertEqual(u.last_name, self.persona_kwargs['last_name'])
            self.assertEqual(u.first_name, self.persona_kwargs['first_name'])

    def test_no_body_cannot_update_role_via_persona_update(self):
        """
        どのユーザーもユーザー情報変更ページから役職を変更することはできない
        """
        persona_count = Persona.objects.count()
        for user in self.members:
            self.prefer_login(user)
            previous_role = user.role
            self.persona_kwargs['role'] = 'adam'
            profile = ProfileFactory(user=user)
            r = self.client.post('/registration/update/', self.persona_kwargs)
            self.assertRedirects(r, '/members/{}/'.format(user.username))
            self.assertEqual(Persona.objects.count(), persona_count)
            u = Persona.objects.get(pk=user.pk)
            self.assertEqual(u.email, self.persona_kwargs['email'])
            self.assertEqual(user.role, previous_role)
            self.assertTrue('messages' in r.cookies, "No messages are appeared")