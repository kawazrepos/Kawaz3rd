from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from .factories import ProjectFactory, CategoryFactory
from kawaz.core.personas.tests.factories import PersonaFactory

class ProjectEditPermissionTestCase(TestCase):
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

class ProjectDeletePermissionTestCase(TestCase):
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

class ProjectViewPermissionTestCase(TestCase):
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

    def test_wille_cannot_view_protected(self):
        '''Tests wille can not view protected'''
        user = PersonaFactory(role='wille')
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

class ProjectAddPermissionTestCase(TestCase):

    def _test_add(self, role, enable):
        user = PersonaFactory(role=role)
        if enable:
            self.assertTrue(user.has_perm('projects.add_project'))
        else:
            self.assertFalse(user.has_perm('projects.add_project'))

    def test_seele_can_add_project(self):
        '''Tests seele user can add project'''
        self._test_add('seele', True)

    def test_nerv_can_add_project(self):
        '''Tests nerv user can add project'''
        self._test_add('nerv', True)

    def test_children_can_add_project(self):
        '''Tests children user can add project'''
        self._test_add('children', True)

    def test_wille_cannot_add_project(self):
        '''Tests wille user cannot add project'''
        self._test_add('wille', False)

    def test_anonymous_cannot_add_project(self):
        '''Tests anonymous user cannot add project'''
        user = AnonymousUser()
        self.assertFalse(user.has_perm('projects.add_project'))


class ProjectJoinPermissionTestCase(TestCase):

    def setUp(self):
        self.project = ProjectFactory()

    def test_authorized_can_join_project(self):
        '''Tests authorized user can join to projects'''
        user = PersonaFactory()
        self.assertTrue(user.has_perm('projects.join_project', self.project))

    def test_wille_cannot_join_project(self):
        '''Tests wille user cannot join to projects'''
        user = PersonaFactory(role='wille')
        self.assertFalse(user.has_perm('projects.join_project', self.project))

    def test_anonymous_cannot_join_project(self):
        '''Tests anonymous user cannot join to projects'''
        user = AnonymousUser()
        self.assertFalse(user.has_perm('projects.join_project', self.project))

    def test_member_cannot_join_project(self):
        '''Tests already member user cannot join to projects'''
        user = PersonaFactory()
        self.project.join(user)
        self.assertFalse(user.has_perm('projects.join_project', self.project))

    def test_anyone_cannot_join_draft_project(self):
        '''Any user can not join to draft projects'''
        project = ProjectFactory(pub_state='draft')
        user = PersonaFactory()
        self.assertFalse(user.has_perm('projects.join_project', project))
        self.assertFalse(project.administrator.has_perm('projects.join_project', project))

class ProjectQuitPermissionTestCase(TestCase):

    def setUp(self):
        self.project = ProjectFactory()

    def test_member_can_quit_project(self):
        '''Tests member can quit from projects'''
        user = PersonaFactory()
        self.project.join(user)
        self.assertTrue(user.has_perm('projects.quit_project', self.project))

    def test_not_member_cannot_quit_project(self):
        '''Tests not member user cannot quit from projects'''
        user = PersonaFactory()
        self.assertFalse(user.has_perm('projects.quit_project', self.project))

    def test_administrator_cannot_quit_project(self):
        '''Tests administrator cannot quit from projects'''
        self.assertFalse(self.project.administrator.has_perm('projects.quit_project', self.project))

