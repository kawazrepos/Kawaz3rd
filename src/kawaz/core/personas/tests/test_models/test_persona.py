from unittest.mock import patch
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from registration.backends.default import DefaultRegistrationBackend
from registration.tests.mock import mock_request
from slack_invitation.slack import SlackInvitationClient

from ..factories import PersonaFactory
from kawaz.core.personas.models import Persona, PersonaManager


class PersonaManagerTestCase(TestCase):
    def test_manager_is_assigned(self):
        """Persona.objectsでPersonaManagerが返る"""
        self.assertTrue(isinstance(Persona.objects, PersonaManager))

    def test_retired(self):
        """PersonaManager.retiredで退会済みのユーザーのみが返る"""
        active_user = PersonaFactory(is_active=True)
        retired_user = PersonaFactory(is_active=False)
        retired = Persona.objects.retired()
        self.assertEqual(len(retired), 1)
        self.assertEqual(retired[0], retired_user)
        self.assertNotIn(active_user, retired)


class PersonaModelTestCase(TestCase):
    def test_create_user(self):
        """Tests it is enable to create user"""
        user = PersonaFactory()
        self.assertEqual(user.first_name, 'Kawaz')
        self.assertEqual(user.last_name, 'Inonaka')

    def test_actives_contains_active_user_only(self):
        """
        Persona.activesのQuerySetは有効なユーザーしか含まない
        """
        user0 = PersonaFactory(username='active')
        user1 = PersonaFactory(is_active=False, username='inactive')
        self.assertEqual(Persona.objects.count(), 2)
        self.assertEqual(Persona.actives.count(), 1)

        self.assertIn(user0, Persona.objects.all())
        self.assertIn(user1, Persona.objects.all())
        self.assertIn(user0, Persona.actives.all())
        self.assertNotIn(user1, Persona.actives.all())

    def test_valid_username_pattern_validation(self):
        """
        VALID_USERNAME_PATTERN に指定された文字列以外は指定できない
        """
        INVALIDS = ('@', '.', '+', 'かわずたん', '蛙', 'ぎぎにゃん', 'السلام عليكم', '안녕하세요', '🍺')
        for invalid in INVALIDS:
            user = PersonaFactory.build(username='foo' + invalid)
            self.assertRaises(ValidationError, user.full_clean)
        VALIDS = ('1', '-', '_')
        for valid in VALIDS:
            user = PersonaFactory.build(username='foo' + valid)
            user.full_clean()

    def test_invalid_username_validation(self):
        """
        INVALID_USERNAMES に指定されているユーザー名は指定できない
        """
        user = PersonaFactory.build(username='my')
        self.assertRaises(ValidationError, user.save)

    def test_automatical_nickname_assign(self):
        """
        The nickname field should automatically assigned from the username
        when the user is created
        """
        user = PersonaFactory.build(nickname='')
        user.save()
        self.assertEqual(user.nickname, user.username)

    def test_is_staff_return_corresponding_value(self):
        """
        `is_staff` property should return True for adam, seele, nerv and False
        for children and wille
        """
        user = PersonaFactory(role='adam')
        self.assertTrue(user.is_staff)
        user = PersonaFactory(role='seele')
        self.assertTrue(user.is_staff)
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.is_staff)
        user = PersonaFactory(role='children')
        self.assertFalse(user.is_staff)
        user = PersonaFactory(role='wille')
        self.assertFalse(user.is_staff)

    def test_is_superuser_return_corresponding_value(self):
        """
        `is_superuser` property should return True for adam and False for seele,
        nerv, children, and wille
        """
        user = PersonaFactory(role='adam')
        self.assertTrue(user.is_superuser)
        user = PersonaFactory(role='seele')
        self.assertFalse(user.is_superuser)
        user = PersonaFactory(role='nerv')
        self.assertFalse(user.is_superuser)
        user = PersonaFactory(role='children')
        self.assertFalse(user.is_superuser)
        user = PersonaFactory(role='wille')
        self.assertFalse(user.is_superuser)

    @override_settings(
        DJANGO_SLACK_INVITATION_TEAM='teamname',
        DJANGO_SLACK_INVITATION_TOKEN='token'
    )
    def test_invite_to_slack(self):
        """
        Personaがacceptされたとき、Slackに自動的に招待する
        """
        request = mock_request()
        backend = DefaultRegistrationBackend()

        with patch.object(SlackInvitationClient, 'invite') as invite:
            new_user = backend.register(
                username='bob', email='bob@example.com',
                request=request)

            profile = new_user.registration_profile
            backend.accept(profile, request=request)

            invite.assert_called_with('bob@example.com')
