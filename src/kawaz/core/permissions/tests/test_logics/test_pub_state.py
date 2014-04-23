from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from permission import add_permission_logic
from permission import remove_permission_logic
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.models import Persona
from ...logics import AdamPermissionLogic
from ...logics import SeelePermissionLogic
from ...logics import NervPermissionLogic
from ...logics import ChildrenPermissionLogic
from ...logics import PubStatePermissionLogic
from ..models import Article


class PubStatePermissionLogicTestCase(TestCase):
    def setUp(self):
        self.users = dict(
                adam=PersonaFactory(role='adam'),
                seele=PersonaFactory(role='seele'),
                nerv=PersonaFactory(role='nerv'),
                children=PersonaFactory(role='children'),
                wille=PersonaFactory(role='wille'),
                anonymous=AnonymousUser(),
                author=PersonaFactory(role='children'),
            )
        self.articles = dict(
                public=Article.objects.create(title="public",
                            author=self.users['author'],
                            pub_state='public'),
                protected=Article.objects.create(title="protected",
                            author=self.users['author'],
                            pub_state='protected'),
                draft=Article.objects.create(title="draft",
                            author=self.users['author'],
                            pub_state='draft'),
            )

    def _test_permission(self, role, obj=None, neg=False, perm='view'):
        user = self.users.get(role)
        obj = self.articles.get(obj, None)
        perm = "permissions.{}_article".format(perm)
        if neg:
            self.assertFalse(user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(user.has_perm(perm, obj=obj),
                "{} should have '{}'".format(role.capitalize(), perm))


    def test_view_permission_without_obj(self):
        """
        Anyone have a potential to see the model
        """
        permission_logic = PubStatePermissionLogic()
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam')
        self._test_permission('seele')
        self._test_permission('nerv')
        self._test_permission('children')
        self._test_permission('wille')
        self._test_permission('anonymous')

    def test_view_permission_with_public(self):
        """
        Anyone can see the public model
        """
        permission_logic = PubStatePermissionLogic()
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'public')
        self._test_permission('seele', 'public')
        self._test_permission('nerv', 'public')
        self._test_permission('children', 'public')
        self._test_permission('wille', 'public')
        self._test_permission('anonymous', 'public')

    def test_view_permission_with_protected(self):
        """
        Authenticated user except wille can see the protected model
        """
        permission_logic = PubStatePermissionLogic()
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'protected')
        self._test_permission('seele', 'protected')
        self._test_permission('nerv', 'protected')
        self._test_permission('children', 'protected')
        self._test_permission('wille', 'protected', neg=True)
        self._test_permission('anonymous', 'protected',neg=True)

    def test_view_permission_with_draft(self):
        """
        Nobody except the author and adam can see the draft model
        """
        permission_logic = PubStatePermissionLogic()
        add_permission_logic(Article, permission_logic)
        self._test_permission('adam', 'draft')
        self._test_permission('seele', 'draft', neg=True)
        self._test_permission('nerv', 'draft', neg=True)
        self._test_permission('children', 'draft', neg=True)
        self._test_permission('wille', 'draft', neg=True)
        self._test_permission('anonymous', 'draft',neg=True)
        self._test_permission('author', 'draft')
