from django.test import TestCase

from .factories import PersonaFactory


class UserTestCase(TestCase):
    def test_create_user(self):
        """Tests it is enable to create user"""
        user = PersonaFactory()
        self.assertEqual(user.first_name, 'Kawaz')
        self.assertEqual(user.last_name, 'Inonaka')
