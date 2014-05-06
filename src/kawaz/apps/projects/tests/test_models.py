from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from .factories import ProjectFactory, CategoryFactory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Project
from ..models import ProjectManager


class CategoryTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        category = CategoryFactory()
        self.assertEqual(str(category), category.label)

class ProjectManagerTestCase(TestCase):

    def setUp(self):
        self.public_project = ProjectFactory()
        self.draft_project = ProjectFactory(pub_state='draft')
        self.protected_project = ProjectFactory(pub_state='protected')
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_project_manager(self):
        '''Tests Project.objects returns ProjectManager instance'''
        self.assertEqual(type(Project.objects), ProjectManager)

    def test_published_with_authorized(self):
        '''
        Tests Project.objects.published() returns QuerySet which contains all active users
        when passed authorized user as its argument.
        '''
        qs = Project.objects.published(self.user)
        self.assertEqual(Project.objects.count(), 3)
        self.assertEqual(qs.count(), 2, 'Queryset have two projects')
        self.assertEqual(qs[0], self.protected_project, 'Queryset have internal project')
        self.assertEqual(qs[1], self.public_project, 'Queryset have public project')

    def test_published_with_wille(self):
        '''
        Tests Project.objects.published() returns QuerySet which contains public users
        when passed users whose role is `wille` as its argument.
        '''
        qs = Project.objects.published(self.wille)
        self.assertEqual(qs.count(), 1, 'Queryset have one project')
        self.assertEqual(qs[0], self.public_project, 'Queryset have public project')

    def test_published_with_anonymous(self):
        '''
        Tests Project.objects.published() returns QuerySet which contains public users
        when passed anonymous user as its argument.
        '''
        qs = Project.objects.published(self.anonymous)
        self.assertEqual(qs.count(), 1, 'Queryset have one project')
        self.assertEqual(qs[0], self.public_project, 'Queryset have public project')

    def test_draft_with_owner(self):
        '''Tests Project.objects.published() with authenticated user returns all publish projects '''
        qs = Project.objects.draft(self.draft_project.administrator)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], self.draft_project)

    def test_draft_with_other(self):
        '''Tests Project.objects.draft() with owner user returns all own draft projects'''
        user = PersonaFactory()
        qs = Project.objects.draft(user)
        self.assertEqual(qs.count(), 0)

    def _create_projects_with_status(self, pub_state='public'):
        d = {}
        for status_tuple in Project.STATUS:
            status = status_tuple[0]
            d.update({status :ProjectFactory(status=status, pub_state=pub_state)})
        return d

    def test_active_with_authenticated(self):
        '''Tests Project.objects.active() with authenticated user returns done, planning or released projects'''
        # Project.objects.public may return 2 projects
        d0 = self._create_projects_with_status(pub_state='public') # +3
        d1 = self._create_projects_with_status(pub_state='protected') # +3
        qs = Project.objects.active(self.user)
        self.assertEqual(qs.count(), 8)

    def test_active_with_anonymous(self):
        '''Tests Project.objects.active() with anonymous user returns done, planning or released projects'''
        # Project.objects.public may return 1 project
        d0 = self._create_projects_with_status(pub_state='public') # +3
        d1 = self._create_projects_with_status(pub_state='protected') # +0
        qs = Project.objects.active(self.anonymous)
        self.assertEqual(qs.count(), 4)


class ProjectModelTestCase(TestCase):
    def test_create_group(self):
        '''Tests to create a group when project was created'''
        project = ProjectFactory()
        group_name = 'project_%s' % project.slug
        group = Group.objects.get(name=group_name)
        self.assertIsNotNone(group)

    def test_str(self):
        '''Tests __str__ returns correct value'''
        project = ProjectFactory()
        self.assertEqual(str(project), project.title)

    def test_creation_group(self):
        '''Tests to create group when project was created'''
        project = ProjectFactory(slug='my-awesome-shooting-game')
        self.assertIsNotNone(project.group)
        self.assertEqual(project.group.name, 'project_my-awesome-shooting-game')

    def test_join_user(self):
        '''Tests can join user correctly'''
        user2 = PersonaFactory()
        project = ProjectFactory()
        self.assertEqual(project.members.count(), 1)
        self.assertEqual(user2.groups.count(), 0)

        project.join(user2)

        self.assertEqual(project.members.count(), 2)
        self.assertEqual(user2.groups.count(), 1)

    def test_join_user_twice(self):
        '''Tests user who already have been joined can't join'''
        user = PersonaFactory()
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
        user = PersonaFactory()

        self.assertRaises(PermissionDenied, project.join, user)

    def test_is_member(self):
        '''Tests is_member returns correct value'''
        user = PersonaFactory()
        user2 = PersonaFactory()
        project = ProjectFactory(administrator=user)
        self.assertEqual(project.members.count(), 1)
        self.assertEqual(project.members.all()[0], user)
        self.assertTrue(project.is_member(user))
        self.assertFalse(project.is_member(user2))

    def test_administrator_is_member(self):
        '''Tests administrator will be added into member automatically'''
        user = PersonaFactory()
        project = ProjectFactory(administrator=user)
        self.assertTrue(project.is_member(user))

    def test_quit(self):
        '''Tests can remove member correctly'''
        project = ProjectFactory()
        user = PersonaFactory()

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
        user = PersonaFactory()

        self.assertRaises(PermissionDenied, project.quit, user)

    def test_anonymous_cant_quit(self):
        '''Tests anonymous can't quit from projects'''
        project = ProjectFactory()
        user = AnonymousUser()

        self.assertRaises(PermissionDenied, project.quit, user)

    def test_get_absolute_url(self):
        '''Tests get_absolute_url() returns '/projects/<slug>/'. '''
        project = ProjectFactory(slug="my-awesome-game")
        self.assertEqual(project.get_absolute_url(), '/projects/my-awesome-game/')

