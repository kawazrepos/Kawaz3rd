from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from .factories import ProjectFactory, CategoryFactory
from kawaz.core.personas.tests.factories import PersonaFactory

class ProjectPermissionTestCase(TestCase):
    def test_administrator_can_edit(self):
        '''Tests administrator can edit a project'''
        project = ProjectFactory()
        self.assertTrue(project.administrator.has_perm('projects.change_project', project))

    def test_members_can_edit(self):
        '''Tests members can edit a project'''
        project = ProjectFactory()
        user = PersonaFactory()
        project.join(user)
        self.assertTrue(user.has_perm('projects.change_project', project))

    def test_others_can_not_edit(self):
        '''Tests others can no edit a project'''
        user = PersonaFactory()
        project = ProjectFactory()
        self.assertFalse(user.has_perm('projects.change_project', project))

    def test_anonymous_can_not_edit(self):
        '''Tests anonymous user can no edit a project'''
        user = AnonymousUser()
        project = ProjectFactory()
        self.assertFalse(user.has_perm('projects.change_project', project))

    def test_administrator_can_delete(self):
        '''Tests administrator can delete a project'''
        project = ProjectFactory()
        self.assertTrue(project.administrator.has_perm('projects.delete_project', project))

    def test_members_can_not_delete(self):
        '''Tests members can not delete a project'''
        project = ProjectFactory()
        user = PersonaFactory()
        project.join(user)
        self.assertFalse(user.has_perm('projects.delete_project', project))

    def test_others_can_not_delete(self):
        '''Tests others can not delete a project'''
        user = PersonaFactory()
        project = ProjectFactory()
        self.assertFalse(user.has_perm('projects.delete_project', project))

    def test_anonymous_can_not_delete(self):
        '''Tests anonymous users can not delete a project'''
        user = AnonymousUser()
        project = ProjectFactory()
        self.assertFalse(user.has_perm('projects.delete_project', project))

    def test_administrator_can_view_draft(self):
        '''Tests administrator can view draft'''
        project = ProjectFactory(pub_state='draft')
        self.assertTrue(project.administrator.has_perm('projects.view_project', project))

    def test_others_can_not_view_draft(self):
        '''Tests others can not view draft'''
        user = PersonaFactory()
        project = ProjectFactory(pub_state='draft')
        self.assertFalse(user.has_perm('projects.view_project', project))

    def test_anonymous_can_not_view_draft(self):
        '''Tests anonymous can not view draft'''
        user = AnonymousUser()
        project = ProjectFactory(pub_state='draft')
        self.assertFalse(user.has_perm('projects.view_project', project))

    def test_administrator_can_view_protected(self):
        '''Tests administrator can view protected'''
        project = ProjectFactory(pub_state='protected')
        self.assertTrue(project.administrator.has_perm('projects.view_project', project))

    def test_others_can_view_protected(self):
        '''Tests others can view protected'''
        user = PersonaFactory()
        project = ProjectFactory(pub_state='protected')
        self.assertTrue(user.has_perm('projects.view_project', project))

    def test_anonymous_can_not_view_protected(self):
        '''Tests anonymous can not view protected'''
        user = AnonymousUser()
        project = ProjectFactory(pub_state='protected')
        self.assertFalse(user.has_perm('projects.view_project', project))

    def test_administrator_can_view_public(self):
        '''Tests administrator can view public'''
        project = ProjectFactory(pub_state='public')
        self.assertTrue(project.administrator.has_perm('projects.view_project', project))

    def test_others_can_view_public(self):
        '''Tests others can view public'''
        user = PersonaFactory()
        project = ProjectFactory(pub_state='public')
        self.assertTrue(user.has_perm('projects.view_project', project))

    def test_anonymous_can_not_view_public(self):
        '''Tests anonymous can view public'''
        user = AnonymousUser()
        project = ProjectFactory(pub_state='public')
        self.assertTrue(user.has_perm('projects.view_project', project))