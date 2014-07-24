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
    not_active_statuses = ['eternal', 'paused', 'done', 'planning']

    def setUp(self):
        def create_user(role):
            if role == 'anonymous':
                return AnonymousUser()
            return PersonaFactory(role=role)

        self.users = {role: create_user(role) for role in ['adam', 'seele', 'nerv', 'children', 'wille', 'anonymous']}
        self.projects = {}
        from kawaz.core.publishments.models import PUB_STATES
        for status in Project.STATUS:
            for pub_state in PUB_STATES:
                key = '{}__{}'.format(status[0], pub_state[0])
                self.projects.update({key: ProjectFactory(status=status[0], pub_state=pub_state[0], administrator__role='seele')})

    def _test_project(self, role, status='active', pub_state='public', neg=False):
        user = self.users[role]
        qs = Project.objects.active(user)
        key = "{}__{}".format(status, pub_state)
        project = self.projects[key]
        if neg:
            self.assertFalse(project in qs,
                             '{} should not show {} {} projects'.format(role, pub_state, status))
        else:
            self.assertTrue(project in qs,
                            '{} should show {} {} projects'.format(role, pub_state, status))

    def test_project_manager(self):
        '''Tests Project.objects returns ProjectManager instance'''
        self.assertEqual(type(Project.objects), ProjectManager)

    def test_active_public(self):
        """
         全てのユーザーでactiveでpublicなプロジェクトを含む
         """
        self._test_project('adam', 'active', 'public')
        self._test_project('seele', 'active', 'public')
        self._test_project('nerv', 'active', 'public')
        self._test_project('children', 'active', 'public')
        self._test_project('wille', 'active', 'public')
        self._test_project('anonymous', 'active', 'public')

    def test_active_protected(self):
        """
         Children以上のユーザーでactiveでprotectedなプロジェクトを含む
         """
        self._test_project('adam', 'active', 'protected')
        self._test_project('seele', 'active', 'protected')
        self._test_project('nerv', 'active', 'protected')
        self._test_project('children', 'active', 'protected')
        self._test_project('wille', 'active', 'protected', neg=True)
        self._test_project('anonymous', 'active', 'protected', neg=True)

    def test_active_draft(self):
        """
         全てのユーザーでactiveでdraftなプロジェクトを含まない
         """
        self._test_project('adam', 'active', 'draft', neg=True)
        self._test_project('seele', 'active', 'draft', neg=True)
        self._test_project('nerv', 'active', 'draft', neg=True)
        self._test_project('children', 'active', 'draft', neg=True)
        self._test_project('wille', 'active', 'draft', neg=True)
        self._test_project('anonymous', 'active', 'draft', neg=True)

    def test_active_with_non_active_status(self):
        """
        pub_stateやuserに関わらず、active以外のプロジェクトは含まれない
        """
        for status in self.not_active_statuses:
            for pub_status in ['public', 'protected', 'draft']:
                self._test_project('adam', status, pub_status, neg=True)
                self._test_project('seele', status, pub_status, neg=True)
                self._test_project('nerv', status, pub_status, neg=True)
                self._test_project('children', status, pub_status, neg=True)
                self._test_project('wille', status, pub_status, neg=True)
                self._test_project('anonymous', status, pub_status, neg=True)

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

