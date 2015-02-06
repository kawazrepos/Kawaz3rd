from django.contrib.auth.models import AnonymousUser
from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.registrations.tests.factories import RegistrationProfileFactory

__author__ = 'giginet'

class GetRegistrationProfilesTestCase(TestCase):

    def _test_get_registration_profiles(self, current_user, status=None):
        if status:
            t = Template(
                """{% load registrations_tags %}"""
                """{% get_registration_profiles status as profiles %}"""
            )
        else:
            t = Template(
                """{% load registrations_tags %}"""
                """{% get_registration_profiles as profiles %}"""
            )
        context = Context({
            'user': current_user,
            'status': status
        })
        # 何も描画されない
        self.assertEqual(t.render(context), '')
        return context['profiles']

    def setUp(self):
        self.users = (
            PersonaFactory(role='adam'),
            PersonaFactory(role='seele'),
            PersonaFactory(role='nerv'),
            PersonaFactory(role='children'),
            PersonaFactory(role='wille'),
            AnonymousUser()
        )
        self.profiles = (
            RegistrationProfileFactory(_status='untreated'),
            RegistrationProfileFactory(_status='accepted'),
            RegistrationProfileFactory(_status='rejected')
        )

    def test_not_staff_cannot_get_any_profiles(self):
        """
        Children, Wille, 非ログインユーザーはNoneが返る
        """
        self.assertIsNone(self._test_get_registration_profiles(self.users[3]))
        self.assertIsNone(self._test_get_registration_profiles(self.users[4]))
        self.assertIsNone(self._test_get_registration_profiles(self.users[5]))

    def test_staff_can_get_all_profiles(self):
        """
        Adam, Seele, Nervは全てのプロフィールを取れる
        """
        self.assertEqual(len(self._test_get_registration_profiles(self.users[0])), 3)
        self.assertEqual(len(self._test_get_registration_profiles(self.users[1])), 3)
        self.assertEqual(len(self._test_get_registration_profiles(self.users[2])), 3)

    def test_staff_can_get_specific_profiles(self):
        """
        Adam, Seele, Nervは特定のプロフィールを取れる
        """
        for user in self.users[:3]:
            for i, status in enumerate(['untreated', 'accepted', 'rejected']):
                profiles = self._test_get_registration_profiles(user, status)
                self.assertEqual(len(profiles), 1)
                self.assertEqual(profiles[0], self.profiles[i])

    def test_staff_cannot_get_profiles_with_invalid_status(self):
        """
        正しくないステータスを渡したとき、TemplateSyntaxErrorが投げられる
        """
        self.assertRaises(TemplateSyntaxError, self._test_get_registration_profiles, self.users[0], 'hogehoge')
        self.assertRaises(TemplateSyntaxError, self._test_get_registration_profiles, self.users[1], 'hogehoge')
        self.assertRaises(TemplateSyntaxError, self._test_get_registration_profiles, self.users[2], 'hogehoge')
        self.assertRaises(TemplateSyntaxError, self._test_get_registration_profiles, self.users[3], 'hogehoge')
        self.assertRaises(TemplateSyntaxError, self._test_get_registration_profiles, self.users[4], 'hogehoge')
        self.assertRaises(TemplateSyntaxError, self._test_get_registration_profiles, self.users[5], 'hogehoge')

