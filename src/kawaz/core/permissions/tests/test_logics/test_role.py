from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from permission import add_permission_logic
from kawaz.core.personas.tests.factories import PersonaFactory
from ...logics import AdamPermissionLogic
from ...logics import SeelePermissionLogic
from ...logics import NervPermissionLogic
from ...logics import ChildrenPermissionLogic
from ..models import PermissionsTestArticle as Article


class ChildrenPermissionLogicTestCase(TestCase):
    roles = ('adam', 'seele', 'nerv', 'children', 'wille', 'anonymous')
    interest_roles = ('adam', 'seele', 'nerv', 'children')
    permission_logic_class = ChildrenPermissionLogic

    def setUp(self):
        self.users = dict(
                adam=PersonaFactory(role='adam'),
                seele=PersonaFactory(role='seele'),
                nerv=PersonaFactory(role='nerv'),
                children=PersonaFactory(role='children'),
                wille=PersonaFactory(role='wille'),
                anonymous=AnonymousUser(),
            )
        self.user = PersonaFactory()
        self.article = Article.objects.create(
                title="public",
                author=self.user,
                pub_state='public')

    def _test_permission(self, role, perm, obj=None, neg=False):
        user = self.users.get(role)
        obj = None if obj is None else self.article
        perm = "permissions.{}_permissionstestarticle".format(perm)
        if neg:
            self.assertFalse(user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(user.has_perm(perm, obj=obj),
                "{} should have '{}'".format(role.capitalize(), perm))

    def _auto_test_permission(self, perm, obj=None):
        positive = set(self.interest_roles)
        negative = set(self.roles).difference(positive)

        for role in positive:
            self._test_permission(role, perm, obj, neg=False)
        for role in negative:
            self._test_permission(role, perm, obj, neg=True)

    def test_add_permission_with_any(self):
        """
        User who is in adam, seele, nerv, children have add permission
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        self._auto_test_permission('add')

    def test_change_permission_with_any(self):
        """
        User who is in adam, seele, nerv, children have add permission
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        self._auto_test_permission('change')
        self._auto_test_permission('change', obj=True)

