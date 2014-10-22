from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.core.urlresolvers import reverse
from kawaz.apps.profiles.tests.factories import ProfileFactory
from kawaz.core.personas.models import Persona
from kawaz.core.personas.tests.factories import PersonaFactory


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


class PersonaAssignAdamViewTestCase(TestCase):
    def setUp(self):
        self.gods = (
                PersonaFactory(role='adam'),
                PersonaFactory(role='seele'),
            )
        self.humans = (
                PersonaFactory(role='nerv'),
                PersonaFactory(role='children'),
                PersonaFactory(role='wille'),
                AnonymousUser(),
            )

    def prefer_login(self, user):
        if user.is_authenticated():
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))

    def test_can_reverse_persona_update_url(self):
        """
        personas_persona_assign_adamが/registration/assign/adam/に割り当てられている
        """
        self.assertEqual(reverse('personas_persona_assign_adam'), '/registration/assign/adam/')

    def test_non_members_cannot_see_persona_assign_adam_view(self):
        """
        ゼーレ以外はアダム化ページを見ることが出来ない
        """
        login_url = settings.LOGIN_URL+'?next=/registration/assign/adam/'
        for user in self.humans:
            self.prefer_login(user)
            r = self.client.get('/registration/assign/adam/')
            self.assertRedirects(r, login_url)

    def test_member_cannot_see_assign_adam(self):
        """
        ゼーレがアダム化ページにアクセスしたとき、NotAllowedが変える
        """
        for user in self.gods:
            self.prefer_login(user)
            r = self.client.get('/registration/assign/adam/')
            self.assertEqual(r.status_code, 405)

    def test_humans_cannot_be_adam(self):
        """
        ゼーレ以外のメンバーはアダム化できない
        """
        login_url = settings.LOGIN_URL+'?next=/registration/assign/adam/'
        for user in self.humans:
            previous_role = getattr(user, 'role', None)
            self.prefer_login(user)
            r = self.client.post('/registration/assign/adam/')
            self.assertRedirects(r, login_url)
            if user.is_authenticated():
                u = Persona.objects.get(pk=user.pk)
                self.assertEqual(u.role, previous_role)

    def test_seele_can_be_adam(self):
        """
        ゼーレはアダム化できる
        """
        persona_count = Persona.objects.count()
        for user in self.gods:
            self.prefer_login(user)
            profile = ProfileFactory(user=user)
            r = self.client.post('/registration/assign/adam/')
            self.assertRedirects(r, '/members/{}/'.format(user.username))
            self.assertEqual(Persona.objects.count(), persona_count)
            u = Persona.objects.get(pk=user.pk)
            self.assertEqual(u.last_name, user.last_name)
            self.assertEqual(u.first_name, user.first_name)
            self.assertEqual(u.role, 'adam')
            self.assertTrue('messages' in r.cookies, "No messages are appeared")


class PersonaAssignSeeleViewTestCase(TestCase):
    def setUp(self):
        self.gods = (
                PersonaFactory(role='adam'),
                PersonaFactory(role='seele'),
            )
        self.humans = (
                PersonaFactory(role='nerv'),
                PersonaFactory(role='children'),
                PersonaFactory(role='wille'),
                AnonymousUser(),
            )

    def prefer_login(self, user):
        if user.is_authenticated():
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))

    def test_can_reverse_persona_update_url(self):
        """
        personas_persona_assign_seeleが/registration/assign/seele/に割り当てられている
        """
        self.assertEqual(reverse('personas_persona_assign_seele'), '/registration/assign/seele/')

    def test_non_members_cannot_see_persona_assign_seele_view(self):
        """
        ゼーレ以外はゼーレ化ページを見ることが出来ない
        """
        login_url = settings.LOGIN_URL+'?next=/registration/assign/seele/'
        for user in self.humans:
            self.prefer_login(user)
            r = self.client.get('/registration/assign/seele/')
            self.assertRedirects(r, login_url)

    def test_member_cannot_see_assign_seele(self):
        """
        ゼーレがゼーレ化ページにアクセスしたとき、NotAllowedが変える
        """
        for user in self.gods:
            self.prefer_login(user)
            r = self.client.get('/registration/assign/seele/')
            self.assertEqual(r.status_code, 405)

    def test_humans_cannot_be_seele(self):
        """
        ゼーレ以外のメンバーはゼーレ化できない
        """
        login_url = settings.LOGIN_URL+'?next=/registration/assign/seele/'
        for user in self.humans:
            previous_role = getattr(user, 'role', None)
            self.prefer_login(user)
            r = self.client.post('/registration/assign/seele/')
            self.assertRedirects(r, login_url)
            if user.is_authenticated():
                u = Persona.objects.get(pk=user.pk)
                self.assertEqual(u.role, previous_role)

    def test_seele_can_be_seele(self):
        """
        ゼーレはゼーレ化できる
        """
        persona_count = Persona.objects.count()
        for user in self.gods:
            self.prefer_login(user)
            profile = ProfileFactory(user=user)
            r = self.client.post('/registration/assign/seele/')
            self.assertRedirects(r, '/members/{}/'.format(user.username))
            self.assertEqual(Persona.objects.count(), persona_count)
            u = Persona.objects.get(pk=user.pk)
            self.assertEqual(u.last_name, user.last_name)
            self.assertEqual(u.first_name, user.first_name)
            self.assertEqual(u.role, 'seele')
            self.assertTrue('messages' in r.cookies, "No messages are appeared")
