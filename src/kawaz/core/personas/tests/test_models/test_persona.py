from django.test import TestCase
from django.core.exceptions import ValidationError

from ..factories import PersonaFactory


class PersonaModelTestCase(TestCase):
    def test_create_user(self):
        """Tests it is enable to create user"""
        user = PersonaFactory()
        self.assertEqual(user.first_name, 'Kawaz')
        self.assertEqual(user.last_name, 'Inonaka')

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
