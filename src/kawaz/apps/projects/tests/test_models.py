from django.test import TestCase
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
    statuses = ['eternal', 'paused', 'done', 'active', 'planning']
    roles = ['adam', 'seele', 'nerv', 'children', 'wille', 'anonymous']
    pub_status = ['public', 'protected', 'draft']

    def setUp(self):
        def create_user(role):
            if role == 'anonymous':
                return AnonymousUser()
            return PersonaFactory(role=role)

        self.users = {role: create_user(role) for role in self.roles}
        self.projects = {}
        from kawaz.core.publishments.models import PUB_STATES
        for status in Project.STATUS:
            for pub_state in PUB_STATES:
                key = '{}__{}'.format(status[0], pub_state[0])
                self.projects.update({key: ProjectFactory(status=status[0], pub_state=pub_state[0], administrator__role='seele')})

    def _test_project(self, method_name, role, status='active', pub_state='public', neg=False, project=None):
        user = self.users[role]
        if not project:
            key = "{}__{}".format(status, pub_state)
            project = self.projects[key]
        method = getattr(Project.objects, method_name)
        qs = method(user)
        if neg:
            self.assertFalse(project in qs,
                             '{} should not show {} {} projects'.format(role, project.pub_state, project.status))
        else:
            self.assertTrue(project in qs,
                            '{} should show {} {} projects'.format(role, project.pub_state, project.status))

    def test_project_manager(self):
        '''Tests Project.objects returns ProjectManager instance'''
        self.assertEqual(type(Project.objects), ProjectManager)

    def test_active_public(self):
        """
         全てのユーザーでactiveでpublicなプロジェクトを含む
         """
        self._test_project('active', 'adam', 'active', 'public')
        self._test_project('active', 'seele', 'active', 'public')
        self._test_project('active', 'nerv', 'active', 'public')
        self._test_project('active', 'children', 'active', 'public')
        self._test_project('active', 'wille', 'active', 'public')
        self._test_project('active', 'anonymous', 'active', 'public')

    def test_active_protected(self):
        """
         Children以上のユーザーでactiveでprotectedなプロジェクトを含む
         """
        self._test_project('active', 'adam', 'active', 'protected')
        self._test_project('active', 'seele', 'active', 'protected')
        self._test_project('active', 'nerv', 'active', 'protected')
        self._test_project('active', 'children', 'active', 'protected')
        self._test_project('active', 'wille', 'active', 'protected', neg=True)
        self._test_project('active', 'anonymous', 'active', 'protected', neg=True)

    def test_active_draft(self):
        """
         全てのユーザーでactiveでdraftなプロジェクトを含まない
         """
        self._test_project('active', 'adam', 'active', 'draft', neg=True)
        self._test_project('active', 'seele', 'active', 'draft', neg=True)
        self._test_project('active', 'nerv', 'active', 'draft', neg=True)
        self._test_project('active', 'children', 'active', 'draft', neg=True)
        self._test_project('active', 'wille', 'active', 'draft', neg=True)
        self._test_project('active', 'anonymous', 'active', 'draft', neg=True)

    def test_active_with_non_active_status(self):
        """
        pub_stateやuserに関わらず、active以外のプロジェクトは含まれない
        """
        not_active_statuses = list(self.statuses)
        not_active_statuses.remove("active")
        for status in not_active_statuses:
            for pub_status in self.pub_status:
                self._test_project('active', 'adam', status, pub_status, neg=True)
                self._test_project('active', 'seele', status, pub_status, neg=True)
                self._test_project('active', 'nerv', status, pub_status, neg=True)
                self._test_project('active', 'children', status, pub_status, neg=True)
                self._test_project('active', 'wille', status, pub_status, neg=True)
                self._test_project('active', 'anonymous', status, pub_status, neg=True)

    def test_recent_planning_recent(self):
        """
        最近作ったPlanningはどのユーザーでも含まれる
        """
        for role in self.roles:
            self._test_project('recently_planned', role, 'planning', 'public')

    def test_recent_planning_past(self):
        """
        90日以上前に作られたPlanningはどのユーザーでも含まれない
        """
        import datetime
        from django.utils import timezone
        past = timezone.now() - datetime.timedelta(days=90)
        # Factoryの引数にcreated_atを渡しても現在に上書きされてしまうので
        # あとで変更して保存している
        old_project = ProjectFactory(status='planning')
        old_project.created_at = past
        old_project.save()
        for role in self.roles:
            self._test_project('recently_planned', role, 'planning', 'public', neg=True, project=old_project)

    def test_recent_planning_not_planning(self):
        """
         planning状態じゃないものはどのユーザーでも含まれない
        """
        not_planning_statuses = list(self.statuses)
        not_planning_statuses.remove('planning')
        for role in self.roles:
            for status in not_planning_statuses:
                self._test_project('recently_planned', role, status, 'public', neg=True)

    def test_archived_with_active_and_planning(self):
        """
        active, planning状態で最近作られた物はどのユーザーでも含まれない
        """
        statuses = ['active', 'planning']
        for role in self.roles:
            for status in statuses:
                self._test_project('archived', role, status, 'public', neg=True)


    def test_archived_with_others(self):
        """
         active, planning以外の状態で最近作られた物はどのユーザーでも含まれる
        """
        ignore_statuses = ['active', 'planning']
        statuses = list(self.statuses)
        for s in ignore_statuses: statuses.remove(s)
        for role in self.roles:
            for status in statuses:
                self._test_project('archived', role, status, 'public')

    def test_archived_with_past_planning(self):
        """
        planningだが、90日以前に作られた物は含まれる
        """
        import datetime
        from django.utils import timezone
        past = timezone.now() - datetime.timedelta(days=90)
        # Factoryの引数にcreated_atを渡しても現在に上書きされてしまうので
        # あとで変更して保存している
        old_project = ProjectFactory(status='planning')
        old_project.created_at = past
        old_project.save()

        for role in self.roles:
            self._test_project('archived', role, project=old_project)



class ProjectModelTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        project = ProjectFactory()
        self.assertEqual(str(project), project.title)

    def test_join_user(self):
        '''Tests can join user correctly'''
        user2 = PersonaFactory()
        project = ProjectFactory()
        self.assertEqual(project.members.count(), 1)

        project.join(user2)

        self.assertEqual(project.members.count(), 2)

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

