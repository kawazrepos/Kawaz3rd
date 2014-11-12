from django.test import TestCase
from registration.backends.default import DefaultRegistrationBackend
from registration.models import RegistrationProfile
from registration.tests.mock import mock_request
from kawaz.core.personas.models import Persona, Profile

__author__ = 'giginet'

class RegistrationActivatedTestCase(TestCase):
    def setUp(self):
        self.backend = DefaultRegistrationBackend()
        self.mock_request = mock_request()

    def test_activated_user_should_be_children(self):
        """
        新規会員登録が承認されたユーザーのactivationが行われたとき、
        signalを受けて権限をwilleからchildrenに変更するsuru
        """
        self.backend.register(username='kawaztan', email='kawaztan@kawaz.org', request=self.mock_request)
        profile = RegistrationProfile.objects.get(user__username='kawaztan')
        self.backend.accept(profile, request=self.mock_request)
        user = profile.user

        # Activateする直前まではwille
        self.assertEqual(user.role, 'wille')
        self.backend.activate(profile.activation_key, request=self.mock_request, password='swordfish')
        # Activateしたらちゃんとchildrenになる
        user = Persona.objects.get(pk=user.pk)
        self.assertEqual(user.role, 'children')

    def test_profile_should_be_created_on_activation(self):
        """
        新規会員登録が承認されたとき、profileが生成される
        """
        self.backend.register(username='kawaztan', email='kawaztan@kawaz.org', request=self.mock_request)
        registration_profile = RegistrationProfile.objects.get(user__username='kawaztan')
        self.backend.accept(registration_profile, request=self.mock_request)
        user = registration_profile.user

        # Activateする直前まではProfileが存在しない
        profile_count = Profile.objects.count()
        self.assertRaises(Profile.objects.get, user=user)
        self.backend.activate(registration_profile.activation_key, request=self.mock_request, password='swordfish')

        # ActivateしたらProfileが生成される
        self.assertEqual(Profile.objects.count(), profile_count + 1)
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
