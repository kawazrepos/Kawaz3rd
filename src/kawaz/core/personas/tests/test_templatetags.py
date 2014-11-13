from django.contrib.auth.models import AnonymousUser
from django.template import Template, Context
from django.test import TestCase
from kawaz.core.personas.tests.factories import ProfileFactory, PersonaFactory

__author__ = 'giginet'

class ProfileTemplateTagTestCase(TestCase):
    def _test_get_my_profile(self, user):
        t = Template(
            """{% load profiles_tags %}"""
            """{% get_my_profile as profile %}"""
        )
        context = Context({
            'user': user
        })
        # 何も描画されない
        self.assertEqual(t.render(context), '')
        return context['profile']

    def test_get_my_profile_with_participants(self):
        """
        get_my_profileタグでProfileを持ってるユーザーについて、自分のプロフィールが取得できる
        """
        profile = ProfileFactory()
        assigned = self._test_get_my_profile(profile.user)
        self.assertEqual(assigned, profile)

    def test_get_my_profile_with_anonymous(self):
        """
         get_my_profileタグで非ログインユーザーについて、Noneが返ってくる
        """
        user = AnonymousUser()
        profile = self._test_get_my_profile(user)
        self.assertIsNone(profile)

    def test_get_my_profile_with_wille(self):
        """
         get_my_profileタグでWilleユーザーについて、Noneが返ってくる
        """
        user = PersonaFactory(role='wille')
        profile = self._test_get_my_profile(user)
        self.assertIsNone(profile)
