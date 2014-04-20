from django.test import TestCase
from django.core.exceptions import ValidationError

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

    def test_permission_of_nerv(self):
        '''Tests when persona role is 'nerv', is_staff become to True automatically.'''
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.is_staff, 'Nerv role is staff')
        self.assertFalse(user.is_superuser, 'Nerv role is not superuser')

    def test_permission_of_seele(self):
        '''Tests when persona role is 'seele', is_staff and is_superuser become to True automatically.'''
        user = PersonaFactory(role='seele')
        self.assertTrue(user.is_staff, 'Seele role is staff')
        self.assertTrue(user.is_superuser, 'Seele role is superuser')

    def test_permission_of_children(self):
        '''Tests children users are not is_staff or is_superuser'''
        user = PersonaFactory(role='children')
        self.assertFalse(user.is_staff, 'Children role is not staff')
        self.assertFalse(user.is_superuser, 'Children role is not superuser')

    def test_permission_of_wille(self):
        '''Tests wille users are not is_staff or is_superuser'''
        user = PersonaFactory(role='wille')
        self.assertFalse(user.is_staff, 'Wille role is not staff')
        self.assertFalse(user.is_superuser, 'Wille role is not superuser')

    def test_permission_of_adam(self):
        '''Tests adam users are not is_staff or is_superuser'''
        user = PersonaFactory(role='adam')
        self.assertFalse(user.is_staff, 'Adam role is not staff')
        self.assertFalse(user.is_superuser, 'Adam role is not superuser')

    def test_change_role(self):
        '''Tests when permission was changed, authorities are abandoned'''
        user = PersonaFactory(role='seele')
        user.role = 'children'
        user.save()
        self.assertFalse(user.is_staff, 'Children role is not staff')
        self.assertFalse(user.is_superuser, 'Children role is not superuser')
