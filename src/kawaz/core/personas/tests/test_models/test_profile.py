from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from ...models import Profile
from ...models import ProfileManager
from ..factories import (PersonaFactory,
                         ProfileFactory,
                         SkillFactory,
                         AccountFactory,
                         ServiceFactory)


class ProfileManagerTestCase(TestCase):

    def setUp(self):
        self.active_profile = ProfileFactory()
        self.inactive_profile = ProfileFactory(
            user=PersonaFactory(is_active=False)
        )
        self.protected_profile = ProfileFactory(pub_state='protected')
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_register_profile_manager(self):
        """
        Profile.objectsがProfileManagerインスタンスを返す
        """
        self.assertTrue(type(Profile.objects), ProfileManager)

    def test_active(self):
        """
        Profile.objects.active()がアクティブユーザーのプロフィールのみ含む
        QSを返す
        """
        qs = Profile.objects.active()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0], self.active_profile)
        self.assertEqual(qs[1], self.protected_profile)

    def test_published_with_authorized(self):
        """
        Children以上のユーザーが渡された場合Profile.objects.published()が
        アクティブユーザーを全てのプロフィールを含むQSを返す
        """
        roles = ('children', 'nerv', 'seele', 'adam')
        for role in roles:
            qs = Profile.objects.published(PersonaFactory(role=role))
            self.assertEqual(qs.count(), 2)
            self.assertEqual(qs[0], self.active_profile)
            self.assertEqual(qs[1], self.protected_profile)

    def test_published_with_wille(self):
        """
        Willeユーザーが渡された場合Profile.objects.published()が内部公開
        プロフィールを除外した全てのアクティブユーザープロフィールを含む
        QSを返す
        """
        qs = Profile.objects.published(self.wille)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], self.active_profile)

    def test_published_with_anonymous(self):
        """
        非ログインユーザーが渡された場合Profile.objects.published()が内部公開
        プロフィールを除外した全てのアクティブユーザープロフィールを含む
        QSを返す
        """
        qs = Profile.objects.published(self.anonymous)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], self.active_profile)


class ProfileModelTestCase(TestCase):

    def test_str(self):
        """str()がニックネームを返す"""
        persona = PersonaFactory(nickname='kawaz tan')
        profile = ProfileFactory(user=persona)
        self.assertEqual(str(profile), 'kawaz tan')

    def test_reverse_access(self):
        """ProfileにPersona._profileで逆アクセスできる"""
        profile = ProfileFactory()
        self.assertEqual(profile.user._profile, profile)

    def test_get_absolute_url(self):
        """Profile.get_absolute_url()が例外を投げる"""
        profile = ProfileFactory()
        self.assertRaises(Exception, profile.get_absolute_url)

    def test_automatically_created_when_persona_created(self):
        """Persona作成時に自動作成される"""
        previous_count = Profile.objects.count()
        persona = PersonaFactory()
        self.assertEqual(previous_count+1, Profile.objects.count())
        self.assertEqual(persona._profile, Profile.objects.last())


class SkillTestCase(TestCase):
    def test_str(self):
        """str()がラベルを返す"""
        skill = SkillFactory()
        self.assertEqual(str(skill), skill.label)


class ServiceTestCase(TestCase):
    def test_str(self):
        """str()がラベルを返す"""
        service = ServiceFactory()
        self.assertEqual(str(service), service.label)


class AccountTestCase(TestCase):
    def test_get_url(self):
        """urlがアカウントのURLを返す"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(account.url, 'http://twitter.com/kawaz_tan/')

    def test_str(self):
        """str()がアカウント名, ユーザー名, サービス名を返す"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(str(account), '{} ({} @ {})'.format(
            account.username,
            account.profile.user.username,
            account.service.label)
        )
