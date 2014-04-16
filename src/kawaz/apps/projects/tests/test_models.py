from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from .factories import ProjectFactory, CategoryFactory
from kawaz.core.auth.tests.factories import UserFactory


class CategoryTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        category = CategoryFactory()
        self.assertEqual(category.__str__(), category.label)

class ProjectTestCase(TestCase):
    def test_create_group(self):
        '''Tests to create a group when project was created'''
        project = ProjectFactory()
        group_name = 'project_%s' % project.slug
        group = Group.objects.get(name=group_name)
        self.assertIsNotNone(group)

    def test_str(self):
        '''Tests __str__ returns correct value'''
        project = ProjectFactory()
        self.assertEqual(project.__str__(), project.title)

    def test_join_user(self):
        '''Tests can join user correctly'''
        user2 = UserFactory()
        project = ProjectFactory()
        self.assertEqual(project.members.count(), 1)
        self.assertEqual(user2.groups.count(), 0)

        project.join(user2)

        self.assertEqual(project.members.count(), 2)
        self.assertEqual(user2.groups.count(), 1)

    def test_join_user_twice(self):
        '''Tests user who already have been joined can't join'''
        user = UserFactory()
        project = ProjectFactory()

        project.join(user)

        self.assertRaises(PermissionDenied, project.join, user)

    def test_join_anonymous(self):
        '''Tests anonymous user can't join'''
        user = AnonymousUser()
        project = ProjectFactory()

        self.assertRaises(PermissionDenied, project.join, user)

    def test_administrator_cannot_join_draft(self):
        '''Tests administrator can't join to draft project.'''
        project = ProjectFactory(pub_state='draft')

        self.assertRaises(PermissionDenied, project.join, project.administrator)

    def test_user_cannot_join_draft(self):
        '''Tests user can't join to draft project.'''
        project = ProjectFactory(pub_state='draft')
        user = UserFactory()

        self.assertRaises(PermissionDenied, project.join, user)

    def test_is_member(self):
        '''Tests is_member returns correct value'''
        user = UserFactory()
        user2 = UserFactory()
        project = ProjectFactory(administrator=user)
        self.assertEqual(project.members.count(), 1)
        self.assertEqual(project.members.all()[0], user)
        self.assertTrue(project.is_member(user))
        self.assertFalse(project.is_member(user2))

    def test_administrator_is_member(self):
        '''Tests administrator will be added into member automatically'''
        user = UserFactory()
        project = ProjectFactory(administrator=user)
        self.assertTrue(project.is_member(user))

    def test_quit(self):
        '''Tests can remove member correctly'''
        project = ProjectFactory()
        user = UserFactory()

        project.join(user)
        self.assertEqual(project.members.count(), 2)

        project.quit(user)
        self.assertEqual(project.members.count(), 1)
        self.assertFalse(user in user.groups.all())

    def test_administrator_cant_quit(self):
        '''Tests administrator can't quit from projects'''
        project = ProjectFactory()

        self.assertRaises(PermissionDenied, project.quit, project.administrator)

    def test_not_member_cant_quit(self):
        '''Tests non member can't quit from projects'''
        project = ProjectFactory()
        user = UserFactory()

        self.assertRaises(PermissionDenied, project.quit, user)

    def test_anonymous_cant_quit(self):
        '''Tests anonymous can't quit from projects'''
        project = ProjectFactory()
        user = AnonymousUser()

        self.assertRaises(PermissionDenied, project.quit, user)

    def test_administrator_can_view_draft(self):
        '''Tests administrator can view draft'''
        project = ProjectFactory(pub_state='draft')
        self.assertTrue(project.administrator.has_perm('projects.view_project', project))

    def test_others_can_not_view_draft(self):
        '''Tests others can not view draft'''
        user = UserFactory()
        project = ProjectFactory(pub_state='draft')
        self.assertFalse(user.has_perm('projects.view_project', project))

    def test_anonymous_can_not_view_draft(self):
        '''Tests anonymous can not view draft'''
        user = AnonymousUser()
        project = ProjectFactory(pub_state='draft')
        self.assertFalse(user.has_perm('projects,view_project', project))

    def test_administrator_can_view_protected(self):
        '''Tests administrator can view protected'''
        project = ProjectFactory(pub_state='protected')
        self.assertTrue(project.administrator.has_perm('projects.view_project', project))

    def test_others_can_view_protected(self):
        '''Tests others can view protected'''
        user = UserFactory()
        project = ProjectFactory(pub_state='protected')
        self.assertTrue(user.has_perm('projects.view_project', project))

    def test_anonymous_can_not_view_protected(self):
        '''Tests anonymous can not view protected'''
        user = AnonymousUser()
        project = ProjectFactory(pub_state='protected')
        self.assertFalse(user.has_perm('projects,view_project', project))

    def test_administrator_can_view_public(self):
        '''Tests administrator can view public'''
        project = ProjectFactory(pub_state='public')
        self.assertTrue(project.administrator.has_perm('projects.view_project', project))

    def test_others_can_view_public(self):
        '''Tests others can view public'''
        user = UserFactory()
        project = ProjectFactory(pub_state='public')
        self.assertTrue(user.has_perm('projects.view_project', project))

    def test_anonymous_can_not_view_public(self):
        '''Tests anonymous can view public'''
        user = AnonymousUser()
        project = ProjectFactory(pub_state='public')
        self.assertTrue(user.has_perm('projects.view_project', project))