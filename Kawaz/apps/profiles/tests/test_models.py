from django.test import TestCase
from .factories import ProfileFactory

class ProfileTestCase(TestCase):
    def test_create_user(self):
        """Tests can access profile via user.get_profile()"""
        profile = ProfileFactory()
        self.assertEqual(profile.user.get_profile(), profile)
