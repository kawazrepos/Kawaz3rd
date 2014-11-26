from django.test import TestCase
from django.core.exceptions import ValidationError

from ..factories import PersonaFactory


class PersonaModelTestCase(TestCase):
    def test_create_user(self):
        """Tests it is enable to create user"""
        user = PersonaFactory()
        self.assertEqual(user.first_name, 'Kawaz')
        self.assertEqual(user.last_name, 'Inonaka')

    def test_valid_username_pattern_validation(self):
        """
        VALID_USERNAME_PATTERN に指定された文字列以外は指定できない
        """
        INVALIDS = ('@', '.', '+')
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
        新規ユーザー作成時にニックネームが指定されていない場合は自動的に
        ユーザー名がアサインされる
        """
        user = PersonaFactory.build(nickname='')
        user.save()
        self.assertEqual(user.nickname, user.username)

    def test_is_staff_return_true_for_adam(self):
        """
        adamに対して`is_staff`が`True`を返す
        """
        user = PersonaFactory(role='adam')
        self.assertTrue(user.is_staff)

    def test_is_staff_return_true_for_seele(self):
        """
        seeleに対して`is_staff`が`True`を返す
        """
        user = PersonaFactory(role='seele')
        self.assertTrue(user.is_staff)

    def test_is_staff_return_true_for_nerv(self):
        """
        nervに対して`is_staff`が`True`を返す
        """
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.is_staff)

    def test_is_staff_return_false_for_children(self):
        """
        childrenに対して`is_staff`が`False`を返す
        """
        user = PersonaFactory(role='children')
        self.assertFalse(user.is_staff)

    def test_is_staff_return_false_for_wille(self):
        """
        willeに対して`is_staff`が`False`を返す
        """
        user = PersonaFactory(role='wille')
        self.assertFalse(user.is_staff)

    def test_is_superuser_return_true_for_adam(self):
        """
        adamに対して`is_superuser`が`True`を返す
        """
        user = PersonaFactory(role='adam')
        self.assertTrue(user.is_superuser)

    def test_is_superuser_return_false_for_seele(self):
        """
        seeleに対して`is_superuser`が`False`を返す
        """
        user = PersonaFactory(role='seele')
        self.assertFalse(user.is_superuser)

    def test_is_superuser_return_false_for_nerv(self):
        """
        nervに対して`is_superuser`が`False`を返す
        """
        user = PersonaFactory(role='nerv')
        self.assertFalse(user.is_superuser)

    def test_is_superuser_return_false_for_children(self):
        """
        childrenに対して`is_superuser`が`False`を返す
        """
        user = PersonaFactory(role='children')
        self.assertFalse(user.is_superuser)

    def test_is_superuser_return_false_for_wille(self):
        """
        willeに対して`is_superuser`が`False`を返す
        """
        user = PersonaFactory(role='wille')
        self.assertFalse(user.is_superuser)
