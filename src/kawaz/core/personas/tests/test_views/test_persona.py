from datetime import timedelta
from itertools import chain
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from ...models import Persona
from ..factories import PersonaFactory
from ..factories import ProfileFactory
from ..factories import ServiceFactory


BASE_URL = 'members'


class PersonaViewTestCaseBase(TestCase):
    def setUp(self):
        # Profileを持たない場合はメンバーとして認められない仕様なので
        # PersonaFactoryではなくProfileFactoryでユーザーを作成している
        self.members = (
                ProfileFactory(user__role='adam').user,
                ProfileFactory(user__role='seele').user,
                ProfileFactory(user__role='nerv').user,
                ProfileFactory(user__role='children').user,
            )
        self.non_members = (
                PersonaFactory(role='wille'),
            )
        self.anonymous = AnonymousUser()

    def prefer_login(self, user):
        if user.is_authenticated():
            # user としてアクセスするためにログイン
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))

class PersonaDetailViewTestCase(PersonaViewTestCaseBase):

    def test_reverse_persona_detail_url(self):
        """
        PersonaDetailViewの逆引き
        """
        # AnonymousUserはusernameすら持たないのでチェックをしていない
        for user in chain(self.members, self.non_members):
            self.assertEqual(
                reverse('personas_persona_detail', kwargs=dict(
                    slug=user.username
                )),
                '/{}/{}/'.format(BASE_URL, user.username),
            )


    def test_access(self):
        """PersonaDetailViewにアクセス可能"""
        profile = ProfileFactory(pub_state='public')
        for user in chain(self.members, self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.get(profile.user.get_absolute_url())
            self.assertTemplateUsed(r, 'personas/persona_detail.html')
            self.assertEqual(r.context_data['object'], profile.user)
            # PersonaDetailViewは'profile'というContextを持つ
            self.assertEqual(r.context_data['profile'], profile)

    def test_access_to_inactive_persona(self):
        """無効化されたユーザーページにはアクセス不可"""
        profile = ProfileFactory(pub_state='public',
                                 user__is_active=False)
        for user in chain(self.members, self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.get(profile.user.get_absolute_url())
            self.assertEqual(r.status_code, 404)

    def test_access_to_wille_persona(self):
        """Willeユーザーページにはアクセス不可"""
        # たとえ Profile を持っていたとしても（通常WilleはProfileを持たない）
        profile = ProfileFactory(pub_state='public',
                                 user__role='wille')
        for user in chain(self.members, self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.get(profile.user.get_absolute_url())
            self.assertEqual(r.status_code, 404)

    def test_access_to_persona_without_profile(self):
        """プロフィールを持たないユーザページにはアクセス不可"""
        invalid_user = PersonaFactory()
        for user in chain(self.members, self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.get(invalid_user.get_absolute_url())
            self.assertEqual(r.status_code, 404)

    @patch('kawaz.core.publishments.perms.PublishmentPermissionLogic')
    def test_access_with_protected_profile(self, PublishmentPermissionLogic):
        """
        PersonaDetailViewの'profile'コンテキストは'profiles.view_profile'
        権限を持たないと参照することができない
        """
        profile = ProfileFactory(pub_state='protected')
        # メンバー（Wille以上）はProtectedなプロフィールでもアクセス可能
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get(profile.user.get_absolute_url())
            self.assertTemplateUsed(r, 'personas/persona_detail.html')
            self.assertEqual(r.context_data['object'], profile.user)
            self.assertEqual(r.context_data['profile'], profile)
        # 非メンバーはProfileコンテキストにはアクセス不可
        for user in chain(self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.get(profile.user.get_absolute_url())
            self.assertTemplateUsed(r, 'personas/persona_detail.html')
            self.assertEqual(r.context_data['object'], profile.user)
            self.assertTrue('profile' not in r.context_data)


class PersonaListViewTestCase(TestCase):
    def setUp(self):
        now = timezone.now()
        self.personas = (
            ProfileFactory(user__last_login=now-timedelta(days=3),
                           user__role='children').user,
            ProfileFactory(user__last_login=now-timedelta(days=2),
                           user__role='children').user,
            ProfileFactory(user__last_login=now-timedelta(days=1),
                           user__role='children').user,
            PersonaFactory(last_login=now-timedelta(days=4),
                           role='wille'),
            PersonaFactory(last_login=now-timedelta(days=5),
                           role='wille'),
        )
        # willeなどを除く有効なメンバー数
        # self.personas を編集した場合は値を適切なものに修正すること
        self.number_of_valid_members = 3

    def test_reverse_persona_list_url(self):
        """
        PersonaListViewの逆引き
        """
        self.assertEqual(
            reverse('personas_persona_list'),
            '/{}/'.format(BASE_URL),
        )

    def test_inactive_personas_are_not_listed(self):
        """
        無効化されたユーザーは一覧に含まれない
        """
        # 検証用にProfileを持つ無効化されたユーザーを追加
        inactive_user = ProfileFactory(user__is_active=False).user
        # 一覧ページへのアクセス
        url = reverse('personas_persona_list')
        r = self.client.get(url)
        self.assertTemplateUsed('persona/persona_list.html')
        self.assertTrue('object_list' in r.context_data)
        object_list = r.context_data['object_list']
        self.assertEqual(object_list.count(), self.number_of_valid_members)
        self.assertFalse(inactive_user in object_list)

    def test_wille_personas_are_not_listed(self):
        """
        Wille権限のユーザーは一覧に含まれない
        """
        # 検証用にProfileを持つWilleユーザーを追加
        wille = ProfileFactory(user__role='wille').user
        # 一覧ページへのアクセス
        url = reverse('personas_persona_list')
        r = self.client.get(url)
        self.assertTemplateUsed('persona/persona_list.html')
        self.assertTrue('object_list' in r.context_data)
        object_list = r.context_data['object_list']
        self.assertEqual(object_list.count(), self.number_of_valid_members)
        self.assertFalse(wille in object_list)

    def test_personas_without_profile_are_not_listed(self):
        """
        プロフィールを持たないユーザーは一覧に含まれない
        """
        # 検証用にProfileを持たないChildrenユーザーを追加
        invalid_user = PersonaFactory(role='children')
        # 一覧ページへのアクセス
        url = reverse('personas_persona_list')
        r = self.client.get(url)
        self.assertTemplateUsed('persona/persona_list.html')
        self.assertTrue('object_list' in r.context_data)
        object_list = r.context_data['object_list']
        self.assertEqual(object_list.count(), 3)
        self.assertFalse(invalid_user in object_list)

    def test_personas_list_order_by_last_login(self):
        """
        ユーザーの一覧は最新ログイン順に並ぶ
        """
        r = self.client.get('/members/')
        self.assertTemplateUsed('personas/persona_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 3,
                         'object_list should have three users')
        self.assertEqual(list[0], self.personas[2], 'public')
        self.assertEqual(list[1], self.personas[1], 'public')
        self.assertEqual(list[2], self.personas[0], 'public')

    def test_personas_list_paginate_by(self):
        """
        ユーザーの一覧は24件ずつ表示される
        """
        # プロフィールを持たないユーザーは一覧に表示されないため
        # PersonaFactoryではなくProfileFactoryを使用している
        [ProfileFactory() for i in range(30)]
        r = self.client.get('/members/')
        self.assertTemplateUsed('personas/persona_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 24,
                         'object_list should have 24 users at once')

        # 30 + 3で33人いるはずで、2ページ目には9人いるはず
        r = self.client.get('/members/?page=2')
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 9)

    def test_personas_list_contains_all_services(self):
        service = ServiceFactory()
        r = self.client.get('/members/')
        self.assertIn('all_services', r.context)
        self.assertIn(service, r.context['all_services'])


class PersonaUpdateViewTestCase(PersonaViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.persona_kwargs = {
            'last_name': '井ノ中',
            'first_name': 'かわず',
            'nickname': 'かわずたん',
            'gender': 'woman',
            'quotes': 'けろーん',
            'email': 'kawaztan@kawaz.org',
            'avatar': None
        }


    def test_reverse_persona_update_url(self):
        """
        PersonaUpdateViewの逆引き
        """
        self.assertEqual(
            reverse('personas_persona_update'),
            '/{}/my/update/'.format(
                BASE_URL,
            ))

    def test_non_members_cannot_access_persona_update_view(self):
        """
        メンバー以外がユーザー編集ページにアクセスした場合は404
        """
        url = reverse('personas_persona_update')
        for user in chain(self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertEqual(r.status_code, 404)

    def test_members_can_access_persona_update_view_of_own(self):
        """
        メンバーはユーザー編集ページにアクセス可能
        """
        url = reverse('personas_persona_update')
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'personas/persona_form.html')
            self.assertTrue('object' in r.context_data)
            self.assertEqual(r.context_data['object'], user)

    def test_non_members_cannot_update_persona(self):
        """
        非メンバーはユーザー情報を編集できない
        """
        url = reverse('personas_persona_update')
        for user in chain(self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.post(url, self.persona_kwargs)
            self.assertEqual(r.status_code, 404)

    def test_members_can_update_own_persona(self):
        """
        メンバーはユーザー情報を編集できる
        """
        url = reverse('personas_persona_update')
        for user in self.members:
            self.prefer_login(user)
            r = self.client.post(url, self.persona_kwargs)
            self.assertRedirects(r, user.get_absolute_url())
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 編集されているかチェック
            u = Persona.objects.get(pk=user.pk)
            self.assertEqual(u.last_name, self.persona_kwargs['last_name'])
            self.assertEqual(u.first_name, self.persona_kwargs['first_name'])

    def test_nobody_cannot_update_role_via_persona_update(self):
        """
        どのユーザーもユーザー情報変更ページから役職を変更することはできない
        """
        url = reverse('personas_persona_update')
        # Adamは最初からAdamなので除外
        for user in self.members[1:]:
            self.prefer_login(user)
            previous_role = user.role
            self.persona_kwargs['role'] = 'adam'
            r = self.client.post(url, self.persona_kwargs)
            self.assertRedirects(r, user.get_absolute_url())
            # 変更されていないことをチェック
            u = Persona.objects.get(pk=user.pk)
            self.assertEqual(user.role, previous_role)
            self.assertNotEqual(user.role, 'adam')
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")


class PersonaAssignAdamViewTestCase(PersonaViewTestCaseBase):

    def test_reverse_persona_assign_adam_url(self):
        """
        personas_persona_assign_adamの逆引き
        """
        self.assertEqual(
            reverse('personas_persona_assign_adam'),
            '/{}/my/assign/adam/'.format(
                BASE_URL,
            ))

    def test_GET_is_not_allowed(self):
        """GETによるアクセスは許可されていない"""
        url = reverse('personas_persona_assign_adam')
        for user in chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get(url)
            # 405: NotAllowed
            self.assertEqual(r.status_code, 405)

    def test_non_seele_cannot_promote_to_adam(self):
        """ゼーレ以外はアダムへの昇格ができない"""
        url = reverse('personas_persona_assign_adam')
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        # Nerv, Children などのメンバーの場合はLOGIN URLにリダイレクト
        for user in chain(self.members[2:]):
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertRedirects(r, login_url)
        # Wille, Anonymous などの非メンバーの場合は404
        for user in chain(self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertEqual(r.status_code, 404)

    def test_seele_can_promote_to_adam(self):
        """ゼーレ以上はアダムへの昇格が可能"""
        url = reverse('personas_persona_assign_adam')
        for user in chain(self.members[:2]):
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertRedirects(r, user.get_absolute_url())
            # キャッシュ更新
            user = Persona.objects.get(pk=user.pk)
            self.assertEqual(user.role, 'adam')


class PersonaAssignSeeleViewTestCase(PersonaViewTestCaseBase):

    def test_reverse_persona_assign_seele_url(self):
        """
        personas_persona_assign_seeleの逆引き
        """
        self.assertEqual(
            reverse('personas_persona_assign_seele'),
            '/{}/my/assign/seele/'.format(
                BASE_URL,
            ))

    def test_GET_is_not_allowed(self):
        """GETによるアクセスは許可されていない"""
        url = reverse('personas_persona_assign_seele')
        for user in chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get(url)
            # 405: NotAllowed
            self.assertEqual(r.status_code, 405)

    def test_non_seele_cannot_promote_to_seele(self):
        """ゼーレ以外はゼーレへの降格ができない"""
        url = reverse('personas_persona_assign_seele')
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        # Nerv, Children などのメンバーの場合はLOGIN URLにリダイレクト
        for user in chain(self.members[2:]):
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertRedirects(r, login_url)
        # Wille, Anonymous などの非メンバーの場合は404
        for user in chain(self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertEqual(r.status_code, 404)

    def test_seele_can_promote_to_seele(self):
        """ゼーレ以上はゼーレへの降格が可能"""
        url = reverse('personas_persona_assign_seele')
        for user in chain(self.members[:2]):
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertRedirects(r, user.get_absolute_url())
            # キャッシュ更新
            user = Persona.objects.get(pk=user.pk)
            self.assertEqual(user.role, 'seele')


class PersonaGraveViewTestCase(PersonaViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.active_user = PersonaFactory(is_active=True)
        self.ghost_user = PersonaFactory(is_active=False)

    def test_grave_url(self):
        """PersonaGraveViewの逆引きができる"""
        self.assertEqual(reverse('personas_persona_grave'), '/members/grave/')

    def test_grave_view(self):
        """チルドレン以上はガフの部屋にアクセスして遺影を表示できる"""
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get('/members/grave/')
            self.assertEqual(r.status_code, 200)
            ghost_users = r.context['object_list']
            self.assertEqual(len(ghost_users), 1)
            self.assertEqual(ghost_users[0], self.ghost_user)

    def test_grave_cannot_view_anonymous(self):
        """非ログインユーザーはガフの部屋を見れない"""
        self.prefer_login(self.anonymous)
        r = self.client.get('/members/grave/')
        self.assertEqual(r.status_code, 302)
