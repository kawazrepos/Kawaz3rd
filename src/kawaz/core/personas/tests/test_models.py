from django.test import TestCase

from .factories import PersonaFactory


class PersonaTestCase(TestCase):
    def test_create_user(self):
        """Tests it is enable to create user"""
        user = PersonaFactory()
        self.assertEqual(user.first_name, 'Kawaz')
        self.assertEqual(user.last_name, 'Inonaka')

    def test_set_nickname(self):
        '''Tests nickname is set automatically'''
        user = PersonaFactory(nickname='')
        self.assertEqual(user.nickname, user.username)
