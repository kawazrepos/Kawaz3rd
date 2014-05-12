import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from .factories import ProjectFactory
from ..models import Project
from kawaz.core.personas.tests.factories import PersonaFactory

class ProjectDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_view_public_project(self):
        '''Tests anonymous user can view public project'''
        project = ProjectFactory()
        r = self.client.get(project.get_absolute_url())
        self.assertTemplateUsed(r, 'projects/project_detail.html')
        self.assertEqual(r.context_data['object'], project)

    def test_administratorized_user_can_view_public_project(self):
        '''Tests administratorized user can view public project'''
        project = ProjectFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(project.get_absolute_url())
        self.assertTemplateUsed(r, 'projects/project_detail.html')
        self.assertEqual(r.context_data['object'], project)

    def test_anonymous_user_can_not_view_protected_project(self):
        '''Tests anonymous user can not view protected project'''
        project = ProjectFactory(pub_state='protected')
        r = self.client.get(project.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, project.get_absolute_url()))

    def test_administratorized_user_can_view_protected_project(self):
        '''Tests administratorized user can view public project'''
        project = ProjectFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(project.get_absolute_url())
        self.assertTemplateUsed(r, 'projects/project_detail.html')
        self.assertEqual(r.context_data['object'], project)

    def test_anonymous_user_can_not_view_draft_project(self):
        '''Tests anonymous user can not view draft project'''
        project = ProjectFactory(pub_state='draft')
        r = self.client.get(project.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, project.get_absolute_url()))

    def test_others_can_not_view_draft_project(self):
        '''
        Tests others can not view draft project
        User will redirect to '/projects/1/update/'
        '''
        project = ProjectFactory(pub_state='draft')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(project.get_absolute_url())
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/{}/update/'.format(project.pk))

    def test_organizer_can_view_draft_project(self):
        '''Tests organizer can view draft project on update view'''
        project = ProjectFactory(pub_state='draft', administrator=self.user)
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(project.get_absolute_url())
        self.assertTemplateUsed(r, 'projects/project_form.html')
        self.assertEqual(r.context_data['object'], project)

class ProjectCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_not_create_view(self):
        '''Tests anonymous user can not view ProjectCreateView'''
        r = self.client.get('/projects/{}/create/'.format(self.user.username))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/{}/create/'.format(self.user.username))

    def test_administratorized_user_can_view_project_create_view(self):
        '''Tests administratorized user can view ProjectCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/projects/{}/create/'.format(self.user.username))
        self.assertTemplateUsed(r, 'projects/project_form.html')
        self.assertFalse('object' in r.context_data)

    def test_anonymous_user_can_not_create_via_create_view(self):
        '''Tests anonymous user can not create project via ProjectCreateView'''
        r = self.client.post('/projects/{}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/{}/create/'.format(self.user.username))

    def test_administratorized_user_can_create_via_create_view(self):
        '''Tests administratorized user can create project via ProjectCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/{}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
        })
        today = datetime.date.today()
        self.assertRedirects(r, '/projects/{0}/{1}/{2}/{3}/1/'.format(self.user.username, today.year, today.month, today.day))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.title, '日記です')

    def test_user_cannot_modify_administrator_id(self):
        '''
        Tests administratorized user cannot modify administrator id.
        In project creation form, `administrator` is exist as hidden field.
        So user can modify `administrator` to invalid values.
        This test checks that `administrator` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/{0}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
            'administrator' : other.pk # crackers attempt to masquerade
        })
        today = datetime.date.today()
        self.assertRedirects(r, '/projects/{0}/{1}/{2}/{3}/1/'.format(self.user.username, today.year, today.month, today.day))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.administrator, self.user)
        self.assertNotEqual(e.administrator, other)


class ProjectUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='administrator_kawaztan')
        self.user.set_password('password')
        self.other = PersonaFactory(username='black_kawaztan')
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.project = ProjectFactory(title='かわずたんだよ☆', administrator=self.user)

    def test_anonymous_user_can_not_view_project_update_view(self):
        '''Tests anonymous user can not view ProjectUpdateView'''
        r = self.client.get('/projects/administrator_kawaztan/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/administrator_kawaztan/1/update/')

    def test_administratorized_user_can_view_project_update_view(self):
        '''
        Tests administratorized user can view ProjectUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/projects/administrator_kawaztan/1/update/')
        self.assertTemplateUsed(r, 'projects/project_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.project)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update project via ProjectUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/projects/administrator_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'クラッカーだよー',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/administrator_kawaztan/1/update/')
        self.assertEqual(self.project.title, 'かわずたんだよ☆')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update project via ProjectUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/projects/administrator_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'いたずら日記です',
            'body' : '黒かわずたんだよーん',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/administrator_kawaztan/1/update/')
        self.assertEqual(self.project.title, 'かわずたんだよ☆')

    def test_administrator_can_update_via_update_view(self):
        '''Tests administrator user can update project via ProjectUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/administrator_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, '/projects/administrator_kawaztan/{0}/{1}/{2}/1/'.format(self.project.publish_at.year, self.project.publish_at.month, self.project.publish_at.day))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')

    def test_user_cannot_modify_administrator_id(self):
        '''
        Tests administratorized user cannot modify administrator id.
        In project update form, `administrator` is exist as hidden field.
        So user can modify `administrator` to invalid values.
        This test checks that `administrator` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/administrator_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'ID書き換えます！',
            'body' : 'うえーい',
            'administrator' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/projects/administrator_kawaztan/{0}/{1}/{2}/1/'.format(self.project.publish_at.year, self.project.publish_at.month, self.project.publish_at.day))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.administrator, self.user)
        self.assertNotEqual(e.administrator, other)
        self.assertEqual(e.title, 'ID書き換えます！')

class ProjectListViewTestCase(TestCase):
    def setUp(self):
        self.projects = (
            ProjectFactory(),
            ProjectFactory(pub_state='protected'),
            ProjectFactory(pub_state='draft'),
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_can_view_only_public_projects(self):
        '''
        Tests anonymous user can view public Project only.
        The protected projects are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/projects/')
        self.assertTemplateUsed('projects/project_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one project')
        self.assertEqual(list[0], self.projects[0])

    def test_wille_can_view_only_public_projects(self):
        '''
        Tests wille user can view public Project only.
        The protected projects are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/projects/')
        self.assertTemplateUsed('projects/project_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one project')
        self.assertEqual(list[0], self.projects[0])

    def test_authenticated_can_view_all_publish_projects(self):
        '''
        Tests authenticated user can view all published projects.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/projects/')
        self.assertTemplateUsed('projects/project_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two projects')
        self.assertEqual(list[0], self.projects[1], 'protected')
        self.assertEqual(list[1], self.projects[0], 'public')

class ProjectAuthorListViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.projects = (
            ProjectFactory(),
            ProjectFactory(administrator=self.user),
            ProjectFactory(pub_state='protected'),
            ProjectFactory(pub_state='protected', administrator=self.user),
            ProjectFactory(pub_state='draft'),
        )

    def test_anonymous_can_view_only_public_projects_of_the_administrator(self):
        '''
        Tests anonymous user can view public Project written by specific administrator only.
        The protected projects are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/projects/{}/'.format(self.user.username))
        self.assertTemplateUsed('projects/project_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one project')
        self.assertEqual(list[0], self.projects[1])

    def test_wille_can_view_only_public_projects_of_the_administrator(self):
        '''
        Tests wille user can view public Project written by specific administrator only.
        The protected projects are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/projects/{}/'.format(self.user.username))
        self.assertTemplateUsed('projects/project_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one project')
        self.assertEqual(list[0], self.projects[1])

    def test_authenticated_can_view_all_publish_projects_of_the_administrator(self):
        '''
        Tests authenticated user can view all published projects written by specific administrator.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/projects/{}/'.format(self.user.username))
        self.assertTemplateUsed('projects/project_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two projects')
        self.assertEqual(list[0], self.projects[3], 'protected')
        self.assertEqual(list[1], self.projects[1], 'public')