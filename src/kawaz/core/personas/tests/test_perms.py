from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from permission import add_permission_logic
from kawaz.core.personas.tests.factories import PersonaFactory
from ..perms import AdamPermissionLogic
from ..perms import SeelePermissionLogic
from ..perms import NervPermissionLogic
from ..perms import ChildrenPermissionLogic
from ..perms import KawazAuthorPermissionLogic
from .models import PersonaTestArticle as Article


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
        perm = "personas.{}_personatestarticle".format(perm)
        if neg:
            self.assertFalse(
                user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(
                user.has_perm(perm, obj=obj),
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

class KawazAuthorPermissionLogicTestCase(TestCase):
    roles = ('adam', 'seele', 'nerv', 'children', 'wille',)
    interest_roles = ('adam', 'seele', 'nerv', 'children')

    def setUp(self):
        self.users = dict(
            adam=PersonaFactory(role='adam'),
            seele=PersonaFactory(role='seele'),
            nerv=PersonaFactory(role='nerv'),
            children=PersonaFactory(role='children'),
            wille=PersonaFactory(role='wille'),
        )
        self.user = PersonaFactory()
        self.permission_logic_class = KawazAuthorPermissionLogic

    def _test_permission(self, role, perm, object_permission=False, author=None, neg=False):
        user = self.users.get(role)
        if not author:
            # Authorが渡されなかったら、自分が作者になる
            author = user
        obj = None
        if object_permission:
            obj = Article.objects.create(
                title="public",
                author=author,
                pub_state='public')
        perm = "personas.{}_personatestarticle".format(perm)
        if neg:
            self.assertFalse(
                user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(
                user.has_perm(perm, obj=obj),
                "{} should have '{}'".format(role.capitalize(), perm))

    def test_add_permission_with_any(self):
        """
        Adam, Seele, Nerv, Childrenは追加権限を持つ
        Willeは追加権限を持たない
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'add')
        self._test_permission('seele', 'add')
        self._test_permission('nerv', 'add')
        self._test_permission('children', 'add')
        self._test_permission('wille', 'add', neg=True)


    def test_change_permission_with_any(self):
        """
        Adam, Seele, Nerv, Childrenはいずれかのオブジェクトの変更権限を持つ
        Willeは変更権限を持たない
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'change')
        self._test_permission('seele', 'change')
        self._test_permission('nerv', 'change')
        self._test_permission('children', 'change')
        self._test_permission('wille', 'change', neg=True)

    def test_change_permission_with_own(self):
        """
        Adam, Seele, Nerv, Childrenは自分の持っているオブジェクトに変更権限を持つ
        Willeは変更権限を持たない
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'change', object_permission=True)
        self._test_permission('seele', 'change', object_permission=True)
        self._test_permission('nerv', 'change', object_permission=True)
        self._test_permission('children', 'change', object_permission=True)
        self._test_permission('wille', 'change', neg=True, object_permission=True)

    def test_change_permission_with_others(self):
        """
        adam以外の全てのユーザーは他人の持っているオブジェクトに変更権限を持たない
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        kwargs = {
            'object_permission': True,
            'author': self.user
        }
        self._test_permission('adam', 'change', **kwargs)
        self._test_permission('seele', 'change', neg=True, **kwargs)
        self._test_permission('nerv', 'change', neg=True, **kwargs)
        self._test_permission('children', 'change', neg=True, **kwargs)
        self._test_permission('wille', 'change', neg=True, **kwargs)

    def test_delete_permission_with_any(self):
        """
        Adam, Seele, Nerv, Childrenはいずれかのオブジェクトの削除権限を持つ
        Willeは削除権限を持たない
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'delete')
        self._test_permission('seele', 'delete')
        self._test_permission('nerv', 'delete')
        self._test_permission('children', 'delete')
        self._test_permission('wille', 'delete', neg=True)

    def test_delete_permission_with_own(self):
        """
        Adam, Seele, Nerv, Childrenは自分の持っているオブジェクトに削除権限を持つ
        Willeは削除権限を持たない
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'delete', object_permission=True)
        self._test_permission('seele', 'delete', object_permission=True)
        self._test_permission('nerv', 'delete', object_permission=True)
        self._test_permission('children', 'delete', object_permission=True)
        self._test_permission('wille', 'delete', neg=True, object_permission=True)

    def test_delete_permission_with_others(self):
        """
        adam以外の全てのユーザーは他人の持っているオブジェクトに削除権限を持たない
        """
        permission_logic = self.permission_logic_class(
            any_permission=True
        )
        add_permission_logic(Article, permission_logic)
        kwargs = {
            'object_permission': True,
            'author': self.user
        }
        self._test_permission('adam', 'delete', **kwargs)
        self._test_permission('seele', 'delete', neg=True, **kwargs)
        self._test_permission('nerv', 'delete', neg=True, **kwargs)
        self._test_permission('children', 'delete', neg=True, **kwargs)
        self._test_permission('wille', 'delete', neg=True, **kwargs)

# TODO: Write the permission test for other permission logics
