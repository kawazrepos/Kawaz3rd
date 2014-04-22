from django.test import TestCase
from django.core.exceptions import ValidationError

from .factories import PersonaFactory


class PersonaModelTestCase(TestCase):
    def test_create_user(self):
        """Tests it is enable to create user"""
        user = PersonaFactory()
        self.assertEqual(user.first_name, 'Kawaz')
        self.assertEqual(user.last_name, 'Inonaka')

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


class PersonaModelPermissionTestCase(TestCase):
    def setUp(self):
        self.users = dict(
                adam=PersonaFactory(role='adam'),
                seele=PersonaFactory(role='seele'),
                nerv=PersonaFactory(role='nerv'),
                children=PersonaFactory(role='children'),
                wille=PersonaFactory(role='wille'),
            )
        self.user = PersonaFactory()

    def _test_permission(self, role, perm, obj=None, negative=False):
        user = self.users.get(role)
        perm = "personas.{}_persona".format(perm)
        if obj == 'self':
            obj = user
        if negative:
            self.assertFalse(user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(user.has_perm(perm, obj=obj),
                "{} should have '{}'".format(role.capitalize(), perm))

    def test_add_permission(self):
        """
        Seele and Nerv should have personas.add_persona but Children and Wille
        """
        self._test_permission('adam', 'add')
        self._test_permission('seele', 'add')
        self._test_permission('nerv', 'add')
        self._test_permission('children', 'add', negative=True)
        self._test_permission('wille', 'add', negative=True)

    def test_view_permission_without_obj(self):
        """
        Nobody except adam should have view permission as non object permission
        """
        self._test_permission('adam', 'view')
        self._test_permission('seele', 'view')
        self._test_permission('nerv', 'view')
        self._test_permission('children', 'view', negative=True)
        self._test_permission('wille', 'view', negative=True)

    def test_view_permission_with_obj(self):
        """
        Seele and Nerv should have view permission but Children and Wille with
        obj
        """
        self._test_permission('adam', 'view', obj=self.user)
        self._test_permission('seele', 'view', obj=self.user)
        self._test_permission('nerv', 'view', obj=self.user)
        self._test_permission('children', 'view', obj=self.user, negative=True)
        self._test_permission('wille', 'view', obj=self.user, negative=True)

    def test_view_permission_with_self(self):
        """
        Anybody should have view permission with self
        """
        self._test_permission('adam', 'view', obj='self')
        self._test_permission('seele', 'view', obj='self')
        self._test_permission('nerv', 'view', obj='self')
        self._test_permission('children', 'view', obj='self')
        self._test_permission('wille', 'view', obj='self')

    def test_change_permission_without_obj(self):
        """
        Nobody except adam should have change permission as non object permission
        """
        self._test_permission('adam', 'change')
        self._test_permission('seele', 'change')
        self._test_permission('nerv', 'change')
        self._test_permission('children', 'change', negative=True)
        self._test_permission('wille', 'change', negative=True)

    def test_change_permission_with_obj(self):
        """
        Seele should have change permission but Nerv, Children, and Wille with
        obj
        """
        self._test_permission('adam', 'change', obj=self.user)
        self._test_permission('seele', 'change', obj=self.user)
        self._test_permission('nerv', 'change', obj=self.user)
        self._test_permission('children', 'change', obj=self.user, negative=True)
        self._test_permission('wille', 'change', obj=self.user, negative=True)

    def test_change_permission_with_self(self):
        """
        Anybody should have change permission with self
        """
        self._test_permission('adam', 'change', obj='self')
        self._test_permission('seele', 'change', obj='self')
        self._test_permission('nerv', 'change', obj='self')
        self._test_permission('children', 'change', obj='self')
        self._test_permission('wille', 'change', obj='self')

    def test_delete_permission_without_obj(self):
        """
        Nobody except adam should have delete permission as non object permission
        """
        self._test_permission('adam', 'delete')
        self._test_permission('seele', 'delete', negative=True)
        self._test_permission('nerv', 'delete', negative=True)
        self._test_permission('children', 'delete', negative=True)
        self._test_permission('wille', 'delete', negative=True)

    def test_delete_permission_with_obj(self):
        """
        Nobody except adam should have delete permission with obj
        """
        self._test_permission('adam', 'delete', obj=self.user)
        self._test_permission('seele', 'delete', obj=self.user, negative=True)
        self._test_permission('nerv', 'delete', obj=self.user, negative=True)
        self._test_permission('children', 'delete', obj=self.user, negative=True)
        self._test_permission('wille', 'delete', obj=self.user, negative=True)

    def test_delete_permission_with_self(self):
        """
        Nobody except adam should have delete permission with self
        """
        self._test_permission('adam', 'delete', obj='self')
        self._test_permission('seele', 'delete', obj=self.user, negative=True)
        self._test_permission('nerv', 'delete', obj=self.user, negative=True)
        self._test_permission('children', 'delete', obj=self.user, negative=True)
        self._test_permission('wille', 'delete', obj=self.user, negative=True)

    def test_activate_permission_without_obj(self):
        """
        Nobody except adam should have activate permission as non object permission
        """
        self._test_permission('adam', 'activate')
        self._test_permission('seele', 'activate')
        self._test_permission('nerv', 'activate')
        self._test_permission('children', 'activate', negative=True)
        self._test_permission('wille', 'activate', negative=True)

    def test_activate_permission_with_obj(self):
        """
        Seele and Nerv should have activate permission but Children and Wille with
        obj
        """
        self._test_permission('adam', 'activate', obj=self.user)
        self._test_permission('seele', 'activate', obj=self.user)
        self._test_permission('nerv', 'activate', obj=self.user)
        self._test_permission('children', 'activate', obj=self.user, negative=True)
        self._test_permission('wille', 'activate', obj=self.user, negative=True)

    def test_activate_permission_with_self(self):
        """
        Seele and Nerv should have activate permission but Children and Wille with
        self
        """
        self._test_permission('adam', 'activate', obj='self')
        self._test_permission('seele', 'activate', obj='self')
        self._test_permission('nerv', 'activate', obj='self')
        self._test_permission('children', 'activate', obj='self', negative=True)
        self._test_permission('wille', 'activate', obj='self', negative=True)

    def test_assign_role_permission_without_obj(self):
        """
        Nobody except adam should have assign_role permission as non object permission
        """
        self._test_permission('adam', 'assign_role')
        self._test_permission('seele', 'assign_role')
        self._test_permission('nerv', 'assign_role', negative=True)
        self._test_permission('children', 'assign_role', negative=True)
        self._test_permission('wille', 'assign_role', negative=True)

    def test_assign_role_permission_with_obj(self):
        """
        Seele should have assign_role permission but Nerv, Children, and Wille with
        obj
        """
        self._test_permission('adam', 'assign_role', obj=self.user)
        self._test_permission('seele', 'assign_role', obj=self.user)
        self._test_permission('nerv', 'assign_role', obj=self.user, negative=True)
        self._test_permission('children', 'assign_role', obj=self.user, negative=True)
        self._test_permission('wille', 'assign_role', obj=self.user, negative=True)

    def test_assign_role_permission_with_self(self):
        """
        Seele should have assign_role permission but Nerv, Children, and Wille with
        self
        """
        self._test_permission('adam', 'assign_role', obj='self')
        self._test_permission('seele', 'assign_role', obj='self')
        self._test_permission('nerv', 'assign_role', obj='self', negative=True)
        self._test_permission('children', 'assign_role', obj='self', negative=True)
        self._test_permission('wille', 'assign_role', obj='self', negative=True)
