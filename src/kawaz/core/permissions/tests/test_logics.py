from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from ..logics import AdamPermissionLogic
from ..logics import SeelePermissionLogic
from ..logics import NervPermissionLogic
from ..logics import ChildrenPermissionLogic
from ..logics import PubStatePermissionLogic
from permission import add_permission_logic
from permission import remove_permission_logic
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.models import Persona
from .models import Article

class RolePermissionLogicTestCase(TestCase):

    def setUp(self):
        [setattr(self, key, PersonaFactory(role=key)) for key in dict(Persona.ROLE_TYPES).keys()]
        self.anonymous = AnonymousUser()

    def test_any_permission_add(self):
        '''
        Tests RolePermissionLogic permits to add the model when any_permission=True
        '''
        logic = ChildrenPermissionLogic(
            any_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.add_article'), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.add_article'))
        self.assertTrue(self.nerv.has_perm('permissions.add_article'))
        self.assertTrue(self.children.has_perm('permissions.add_article'))
        self.assertFalse(self.wille.has_perm('permissions.add_article'))
        self.assertFalse(self.anonymous.has_perm('permissions.add_article'))
        remove_permission_logic(Article, logic)

    def test_any_permission_change(self):
        '''
        Tests RolePermissionLogic permits to change the model when any_permission=True
        '''
        logic = ChildrenPermissionLogic(
            any_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article'), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.change_article'))
        self.assertTrue(self.nerv.has_perm('permissions.change_article'))
        self.assertTrue(self.children.has_perm('permissions.change_article'))
        self.assertFalse(self.wille.has_perm('permissions.change_article'))
        self.assertFalse(self.anonymous.has_perm('permissions.change_article'))
        remove_permission_logic(Article, logic)

    def test_any_permission_delete(self):
        '''
        Tests RolePermissionLogic permits to delete the model when any_permission=True
        '''
        logic = ChildrenPermissionLogic(
            any_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.delete_article'), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.delete_article'))
        self.assertTrue(self.nerv.has_perm('permissions.delete_article'))
        self.assertTrue(self.children.has_perm('permissions.delete_article'))
        self.assertFalse(self.wille.has_perm('permissions.delete_article'))
        self.assertFalse(self.anonymous.has_perm('permissions.delete_article'))
        remove_permission_logic(Article, logic)

    def test_add_permission(self):
        '''
        Tests RolePermissionLogic permits to add the model by add_permission value.
        '''
        logic = ChildrenPermissionLogic(
            add_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.add_article'), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.add_article'))
        self.assertTrue(self.nerv.has_perm('permissions.add_article'))
        self.assertTrue(self.children.has_perm('permissions.add_article'))
        self.assertFalse(self.wille.has_perm('permissions.add_article'))
        self.assertFalse(self.anonymous.has_perm('permissions.add_article'))
        remove_permission_logic(Article, logic)

    def test_add_permission_without_add_permission(self):
        '''
        Tests RolePermissionLogic permits to add the model by add_permission value with add_permission=False.
        '''
        logic = ChildrenPermissionLogic()
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        add_permission_logic(Article, logic)
        self.assertFalse(self.seele.has_perm('permissions.add_article', obj=article))
        self.assertFalse(self.nerv.has_perm('permissions.add_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.add_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.add_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.add_article', obj=article))
        remove_permission_logic(Article, logic)

    def test_add_permission_with_obj(self):
        '''
        Tests RolePermissionLogic without object with add always returns False
        '''
        logic = ChildrenPermissionLogic(
            add_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertFalse(self.seele.has_perm('permissions.change_article'))
        self.assertFalse(self.nerv.has_perm('permissions.change_article'))
        self.assertFalse(self.children.has_perm('permissions.change_article'))
        self.assertFalse(self.wille.has_perm('permissions.change_article'))
        self.assertFalse(self.anonymous.has_perm('permissions.change_article'))
        remove_permission_logic(Article, logic)

    def test_change_permission_without_obj_change(self):
        '''
        Tests RolePermissionLogic without object with change always returns False
        '''
        logic = ChildrenPermissionLogic(
            change_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertFalse(self.seele.has_perm('permissions.change_article'))
        self.assertFalse(self.nerv.has_perm('permissions.change_article'))
        self.assertFalse(self.children.has_perm('permissions.change_article'))
        self.assertFalse(self.wille.has_perm('permissions.change_article'))
        self.assertFalse(self.anonymous.has_perm('permissions.change_article'))
        remove_permission_logic(Article, logic)

    def test_delete_permission_without_obj_delete(self):
        '''
        Tests RolePermissionLogic without object with delete always returns False
        '''
        logic = ChildrenPermissionLogic(
            delete_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertFalse(self.seele.has_perm('permissions.delete_article'))
        self.assertFalse(self.nerv.has_perm('permissions.delete_article'))
        self.assertFalse(self.children.has_perm('permissions.delete_article'))
        self.assertFalse(self.wille.has_perm('permissions.delete_article'))
        self.assertFalse(self.anonymous.has_perm('permissions.delete_article'))
        remove_permission_logic(Article, logic)

    def test_adam_permission_logic_change(self):
        '''
        Tests AdamPermissionLogic permits adam users only.
        '''
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        logic = AdamPermissionLogic(
            change_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertFalse(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.change_article'))
        remove_permission_logic(Article, logic)

    def test_seele_permission_logic_change(self):
        '''
        Tests SeelePermissionLogic permits changing seele or adam users only.
        '''
        logic = SeelePermissionLogic(
            change_permission=True
        )
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.change_article'))
        remove_permission_logic(Article, logic)

    def test_nerv_permission_logic_change(self):
        '''
        Tests NervPermissionLogic permits changing nerv, seele or adam users.
        '''
        logic = NervPermissionLogic(
            change_permission=True
        )
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertTrue(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.change_article'))
        remove_permission_logic(Article, logic)

    def test_children_permission_logic_change(self):
        '''
        Tests ChildrenPermissionLogic permits changing children, nerv, seele or adam users.
        '''
        logic = ChildrenPermissionLogic(
            change_permission=True
        )
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.change_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.change_article', obj=article))
        self.assertTrue(self.nerv.has_perm('permissions.change_article', obj=article))
        self.assertTrue(self.children.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.change_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.change_article'))
        remove_permission_logic(Article, logic)

    def test_adam_permission_logic_delete(self):
        '''
        Tests AdamPermissionLogic permits deletion adam users only.
        '''
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        logic = AdamPermissionLogic(
            delete_permission=True
        )
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.delete_article', obj=article), 'adam has all permissions')
        self.assertFalse(self.seele.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.nerv.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.delete_article'))
        remove_permission_logic(Article, logic)

    def test_seele_permission_logic_delete(self):
        '''
        Tests SeelePermissionLogic permits deletion seele or adam users only.
        '''
        logic = SeelePermissionLogic(
            delete_permission=True
        )
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.delete_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.nerv.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.delete_article'))
        remove_permission_logic(Article, logic)

    def test_nerv_permission_logic_delete(self):
        '''
        Tests NervPermissionLogic permits deletion nerv, seele or adam users.
        '''
        logic = NervPermissionLogic(
            delete_permission=True
        )
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.delete_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.delete_article', obj=article))
        self.assertTrue(self.nerv.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.children.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.delete_article'))
        remove_permission_logic(Article, logic)

    def test_children_permission_logic_delete(self):
        '''
        Tests ChildrenPermissionLogic permits deletion children, nerv, seele or adam users.
        '''
        logic = ChildrenPermissionLogic(
            delete_permission=True
        )
        article = Article.objects.create(title='hoge', written_by=PersonaFactory())
        add_permission_logic(Article, logic)
        self.assertTrue(self.adam.has_perm('permissions.delete_article', obj=article), 'adam has all permissions')
        self.assertTrue(self.seele.has_perm('permissions.delete_article', obj=article))
        self.assertTrue(self.nerv.has_perm('permissions.delete_article', obj=article))
        self.assertTrue(self.children.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.wille.has_perm('permissions.delete_article', obj=article))
        self.assertFalse(self.anonymous.has_perm('permissions.delete_article'))
        remove_permission_logic(Article, logic)

class PubStatePermissionLogicTestCase(TestCase):

    def setUp(self):
        self.users = dict(
                adam=PersonaFactory(role='adam'),
                seele=PersonaFactory(role='seele'),
                nerv=PersonaFactory(role='nerv'),
                children=PersonaFactory(role='children'),
                wille=PersonaFactory(role='wille'),
                anonymous=AnonymousUser()
            )
        self.user = PersonaFactory()

    def test_without_obj(self):
        '''
        Tests PubStatePermissionLogic don't treat non object permission.
        '''
        logic = PubStatePermissionLogic(author_field_name='written_by', pub_state_field_name='publish_status')
        add_permission_logic(Article, logic)
        self.assertFalse(self.users.get('seele').has_perm('permissions.view_article'), 'do not treat non object permission')
        self.assertFalse(self.users.get('nerv').has_perm('permissions.view_article'), 'do not treat non object permission')
        self.assertFalse(self.users.get('children').has_perm('permissions.view_article'), 'do not treat non object permission')
        self.assertFalse(self.users.get('wille').has_perm('permissions.view_article'), 'do not treat non object permission')
        self.assertFalse(self.users.get('anonymous').has_perm('permissions.view_article'), 'do not treat non object permission')
        remove_permission_logic(Article, logic)

    def test_pub_state_is_public(self):
        '''
        Tests when pub_state is public, everyone can see the article.
        '''
        logic = PubStatePermissionLogic(author_field_name='written_by', pub_state_field_name='publish_status')
        article = Article.objects.create(title='hoge', written_by=self.user)
        add_permission_logic(Article, logic)
        self.assertTrue(self.users.get('seele').has_perm('permissions.view_article', obj=article), 'everyone can see public object')
        self.assertTrue(self.users.get('nerv').has_perm('permissions.view_article', obj=article), 'everyone can see public object')
        self.assertTrue(self.users.get('children').has_perm('permissions.view_article', obj=article), 'everyone can see public object')
        self.assertTrue(self.users.get('wille').has_perm('permissions.view_article', obj=article), 'everyone can see public object')
        self.assertTrue(self.users.get('anonymous').has_perm('permissions.view_article', obj=article), 'everyone can see public object')
        remove_permission_logic(Article, logic)

    def test_pub_state_is_protected_with_authorized_general_users(self):
        '''
        Tests when pub_state is private, authorized users who has the role 'seele', 'nerv', 'adam' or 'children' can see the article.
        '''
        logic = PubStatePermissionLogic(author_field_name='written_by', pub_state_field_name='publish_status')
        article = Article.objects.create(title='hoge', written_by=self.user, publish_status='protected')
        add_permission_logic(Article, logic)
        self.assertTrue(self.users.get('seele').has_perm('permissions.view_article', obj=article), 'authorized can see protected object')
        self.assertTrue(self.users.get('nerv').has_perm('permissions.view_article', obj=article), 'everyone can see public object')
        self.assertTrue(self.users.get('children').has_perm('permissions.view_article', obj=article), 'everyone can see public object')
        remove_permission_logic(Article, logic)

    def test_pub_state_is_protected_with_authorized_wille_users(self):
        '''
        Tests when pub_state is private, authorized users who has the role 'wille' cannot see the article.
        '''
        logic = PubStatePermissionLogic(author_field_name='written_by', pub_state_field_name='publish_status')
        article = Article.objects.create(title='hoge', written_by=self.user, publish_status='protected')
        add_permission_logic(Article, logic)
        self.assertFalse(self.users.get('wille').has_perm('permissions.view_article', obj=article), 'wille user cannot see protected object')
        remove_permission_logic(Article, logic)

    def test_pub_state_is_protected_with_anonymous_users(self):
        '''
        Tests when pub_state is private, anonymous users cannot see the article.
        '''
        logic = PubStatePermissionLogic(author_field_name='written_by', pub_state_field_name='publish_status')
        article = Article.objects.create(title='hoge', written_by=self.user, publish_status='protected')
        add_permission_logic(Article, logic)
        self.assertFalse(self.users.get('anonymous').has_perm('permissions.view_article', obj=article), 'anonymous cannot see protected object')
        remove_permission_logic(Article, logic)

    def test_pub_state_is_draft_with_author(self):
        '''
        Tests when pub_state is draft, author can see the article
        '''
        logic = PubStatePermissionLogic(author_field_name='written_by', pub_state_field_name='publish_status')
        article = Article.objects.create(title='hoge', written_by=self.user, publish_status='draft')
        add_permission_logic(Article, logic)
        self.assertTrue(self.user.has_perm('permissions.view_article', obj=article), 'author can see draft object')
        remove_permission_logic(Article, logic)

    def test_pub_state_is_draft_with_other_users(self):
        '''
        Tests when pub_state is draft, all users who don't create this object cannot see it.
        '''
        logic = PubStatePermissionLogic(author_field_name='written_by', pub_state_field_name='publish_status')
        article = Article.objects.create(title='hoge', written_by=self.user, publish_status='draft')
        add_permission_logic(Article, logic)
        self.assertTrue(self.users.get('adam').has_perm('permissions.view_article', obj=article), '''adam can see other's draft object''')
        self.assertFalse(self.users.get('seele').has_perm('permissions.view_article', obj=article), 'others cannnot see draft object')
        self.assertFalse(self.users.get('nerv').has_perm('permissions.view_article', obj=article), 'others cannnot see draft object')
        self.assertFalse(self.users.get('children').has_perm('permissions.view_article', obj=article), 'others cannnot see draft object')
        self.assertFalse(self.users.get('wille').has_perm('permissions.view_article', obj=article), 'others cannnot see draft object')
        self.assertFalse(self.users.get('anonymous').has_perm('permissions.view_article', obj=article), 'others cannnot see draft object')
        remove_permission_logic(Article, logic)
