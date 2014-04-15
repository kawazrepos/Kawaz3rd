from django.test import TestCase

from .factories import UserFactory


class UserTestCase(TestCase):
    def test_create_user(self):
        """Tests it is enable to create user"""
        user = UserFactory()
        self.assertEqual(user.first_name, 'Kawaz')
        self.assertEqual(user.last_name, 'Inonaka')
