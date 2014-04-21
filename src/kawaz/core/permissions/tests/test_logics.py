from django.test import TestCase
from permission import add_permission_logic, remove_permission_logic
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.models import Persona
from ..logics import AdamPermissionLogic, SeelePermissionLogic, NervPermissionLogic, ChildrenPermissionLogic
from .models import Article

class RolePermissionLogicTestCase(TestCase):
    def setUp(self):
        [setattr(self, key, PersonaFactory(role=key)) for key in dict(Persona.ROLE_TYPES).keys()]

    def test_add_permission(self):
        '''
        Tests to check that RolePermissionLogic permits to add the model by add_permission value.
        '''
        logic = AdamPermissionLogic(
            add_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.add_article'), 'adam has all permissions')
        self.assertFalse(self.seele.has_perm('permissions.add_article'))
        self.assertFalse(self.nerv.has_perm('permissions.add_article'))
        self.assertFalse(self.children.has_perm('permissions.add_article'))
        self.assertFalse(self.wille.has_perm('permissions.add_article'))
        remove_permission_logic(Article, logic)

    def test_adam_permission_logic(self):
        '''
        Tests to check that AdamPermissionLogic permits adam users only.
        '''
        article = Article.objects.create(title='hoge')
        logic = AdamPermissionLogic(
            change_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertFalse(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        remove_permission_logic(Article, logic)

    def test_seele_permission_logic(self):
        '''
        Tests to check that SeelePermissionLogic permits seele or adam users only.
        '''
        logic = SeelePermissionLogic(
            change_permission=True
        )
        article = Article.objects.create(title='hoge')
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        remove_permission_logic(Article, logic)

    def test_nerv_permission_logic(self):
        '''
        Tests to check that NervPermissionLogic permits nerv, seele or adam users.
        '''
        logic = NervPermissionLogic(
            change_permission=True
        )
        article = Article.objects.create(title='hoge')
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertTrue(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        remove_permission_logic(Article, logic)

    def test_children_permission_logic(self):
        '''
        Tests to check that ChildrenPermissionLogic permits children, nerv, seele or adam users.
        '''
        logic = ChildrenPermissionLogic(
            change_permission=True
        )
        article = Article.objects.create(title='hoge')
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertTrue(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertTrue(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        remove_permission_logic(Article, logic)
