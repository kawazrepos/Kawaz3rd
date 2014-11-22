import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from .factories import ProjectFactory
from .factories import CategoryFactory
from ..models import Project
from kawaz.core.personas.tests.factories import PersonaFactory

class ViewTestCaseBase(TestCase):
    def setUp(self):
        self.members = (
                PersonaFactory(role='adam'),
                PersonaFactory(role='seele'),
                PersonaFactory(role='nerv'),
                PersonaFactory(role='children'),
            )
        self.non_members = (
                PersonaFactory(role='wille'),
                AnonymousUser(),
            )
        self.platform = ProjectFactory()
        self.category = CategoryFactory()

    def prefer_login(self, user):
        if user.is_authenticated():
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))

class ProjectDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_view_public_project(self):
        '''Tests anonymous user can view public project'''
        project = ProjectFactory()
        r = self.client.get(project.get_absolute_url())
        self.assertTemplateUsed(r, 'projects/project_detail.html')
        self.assertEqual(r.context_data['object'], project)

    def test_authorized_user_can_view_public_project(self):
        '''Tests authorized user can view public project'''
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

    def test_authorized_user_can_view_protected_project(self):
        '''Tests authorized user can view public project'''
        project = ProjectFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(project.get_absolute_url())
        self.assertTemplateUsed(r, 'projects/project_detail.html')
        self.assertEqual(r.context_data['object'], project)

    def test_wille_user_can_not_view_protected_project(self):
        '''
        Tests wille user can not view any protected projects
        '''
        project = ProjectFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get(project.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, project.get_absolute_url()))


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

    def test_administrator_can_view_draft_project(self):
        '''Tests administrator can view draft project on update view'''
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
        self.category = CategoryFactory()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_not_create_view(self):
        '''Tests anonymous user can not view ProjectCreateView'''
        r = self.client.get('/projects/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/create/')

    def test_wille_user_can_not_view_project_create_view(self):
        '''Tests wille user can not view ProjectCreateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/projects/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/create/')

    def test_authorized_user_can_view_project_create_view(self):
        '''Tests authorized user can view ProjectCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/projects/create/')
        self.assertTemplateUsed(r, 'projects/project_form.html')
        self.assertFalse('object' in r.context_data)

    def test_anonymous_user_can_not_create_via_create_view(self):
        '''Tests anonymous user can not create project via ProjectCreateView'''
        r = self.client.post('/projects/create/', {
            'pub_state' : 'public',
            'title' : '音楽ファンタジー',
            'status' : 'planning',
            'body' : 'ルシがファルシでコクーン',
            'slug' : 'music-fantasy',
            'category' : self.category.pk
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/create/')

    def test_wille_user_can_not_create_via_create_view(self):
        '''Tests wille user can not create project via ProjectCreateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/projects/create/', {
            'pub_state' : 'public',
            'title' : '音楽ファンタジー',
            'status' : 'planning',
            'body' : 'ルシがファルシでコクーン',
            'slug' : 'music-fantasy',
            'category' : self.category.pk
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/create/')

    def test_authorized_user_can_create_via_create_view(self):
        '''Tests authorized user can create project via ProjectCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/create/', {
            'pub_state' : 'public',
            'title' : '音楽ファンタジー',
            'status' : 'planning',
            'body' : 'ルシがファルシでコクーン',
            'slug' : 'music-fantasy',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/projects/music-fantasy/')
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.title, '音楽ファンタジー')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_authorized_user_can_create_via_create_view(self):
        '''
        プロジェクト作成時にlast_modifierがセットされる
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/create/', {
            'pub_state' : 'public',
            'title' : '音楽ファンタジー',
            'status' : 'planning',
            'body' : 'ルシがファルシでコクーン',
            'slug' : 'music-fantasy',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/projects/music-fantasy/')
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.last_modifier, self.user)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_user_cannot_modify_administrator_id(self):
        '''
        Tests authorized user cannot modify administrator id.
        In project creation form, `administrator` is exist as hidden field.
        So user can modify `administrator` to invalid values.
        This test checks that `administrator` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/create/', {
            'pub_state' : 'public',
            'title' : '音楽ファンタジー',
            'status' : 'planning',
            'body' : 'ルシがファルシでコクーン',
            'slug' : 'music-fantasy',
            'category' : self.category.pk,
            'administrator' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/projects/music-fantasy/')
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
        self.project = ProjectFactory(title='かわずたんのゲームだよ☆', administrator=self.user)
        self.category = CategoryFactory()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_not_view_project_update_view(self):
        '''Tests anonymous user can not view ProjectUpdateView'''
        r = self.client.get('/projects/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/1/update/')

    def test_wille_user_can_not_view_project_update_view(self):
        '''Tests wille user can not view ProjectUpdateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/projects/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/1/update/')

    def test_authorized_user_can_view_project_update_view(self):
        '''
        Tests authorized user can view ProjectUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/projects/1/update/')
        self.assertTemplateUsed(r, 'projects/project_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.project)

    def test_member_can_view_project_update_view(self):
        '''
        Tests project members can view ProjectUpdateView
        '''
        self.project.join(self.other)
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.get('/projects/1/update/')
        self.assertTemplateUsed(r, 'projects/project_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.project)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update project via ProjectUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : 'クラッカーだよー',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/1/update/')
        self.assertEqual(self.project.title, 'かわずたんのゲームだよ☆')

    def test_wille_user_can_not_update_via_update_view(self):
        '''
        Tests wille user can not update project via ProjectUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : '外部ユーザーだよーん',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/1/update/')
        self.assertEqual(self.project.title, 'かわずたんのゲームだよ☆')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update project via ProjectUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : 'いたずら日記です',
            'body' : '黒かわずたんだよーん',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/projects/1/update/')
        self.assertEqual(self.project.title, 'かわずたんのゲームだよ☆')

    def test_administrator_can_update_via_update_view(self):
        '''Tests administrator user can update project via ProjectUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/projects/{}/'.format(self.project.slug))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_member_can_update_via_update_view(self):
        '''Tests project member can update project via ProjectUpdateView'''
        self.project.join(self.other)
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/projects/{}/'.format(self.project.slug))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_set_last_modifier_via_update_view(self):
        """
        プロジェクト編集時にlast_modifierがセットされる
        """
        self.project.join(self.other)
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/projects/{}/'.format(self.project.slug))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.last_modifier, self.other)
        self.assertNotEqual(e.last_modifier, e.administrator)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_user_cannot_update_slug(self):
        '''Tests anyone cannot update prject's slug'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        old_slug = self.project.slug
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk,
            'slug' : 'new-slug'
        })
        self.assertRedirects(r, '/projects/{}/'.format(self.project.slug))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.slug, old_slug)
        self.assertNotEqual(e.slug, 'new-slug')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_user_cannot_modify_administrator_id(self):
        '''
        Tests authorized user cannot modify administrator id.
        In project update form, `administrator` is exist as hidden field.
        So user can modify `administrator` to invalid values.
        This test checks that `administrator` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/1/update/', {
            'pub_state' : 'public',
            'title' : 'ID書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk,
            'administrator' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/projects/{}/'.format(self.project.slug))
        self.assertEqual(Project.objects.count(), 1)
        e = Project.objects.get(pk=1)
        self.assertEqual(e.administrator, self.user)
        self.assertNotEqual(e.administrator, other)
        self.assertEqual(e.title, 'ID書き換えます！')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

class ProjectDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.other = PersonaFactory()
        self.other.set_password('password')
        self.other.save()
        self.project = ProjectFactory(administrator=self.user)

    def test_administrator_can_delete_via_project_delete_view(self):
        '''
        Tests administrators can delete its own projects via ProjectDeleteView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/1/delete/', {})
        self.assertEqual(Project.objects.count(), 0)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_member_cannot_delete_via_project_delete_view(self):
        '''
        Tests members cannot delete its projects via ProjectDeleteView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        self.project.join(self.other)
        r = self.client.post('/projects/1/delete/', {})
        self.assertEqual(Project.objects.count(), 1)

    def test_other_cannot_delete_via_project_delete_view(self):
        '''
        Tests others cannot delete projects via ProjectDeleteView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/projects/1/delete/', {})
        self.assertEqual(Project.objects.count(), 1)

    def test_wille_cannot_delete_via_project_delete_view(self):
        '''
        Tests wille cannot delete projects via ProjectDeleteView
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/projects/1/delete/', {})
        self.assertEqual(Project.objects.count(), 1)

    def test_anonymous_cannot_delete_via_project_delete_view(self):
        '''
        Tests anonymous cannot delete projects via ProjectDeleteView
        '''
        r = self.client.post('/projects/1/delete/', {})
        self.assertEqual(Project.objects.count(), 1)


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


class ProjectArchiveViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.projects = (
            ProjectFactory(status='eternal'),
            ProjectFactory(status='active'),
            ProjectFactory(pub_state='protected', status='planning'),
            ProjectFactory(pub_state='protected', status='done'),
            ProjectFactory(pub_state='draft')
        )

    def test_members_can_view_all_archive(self):
        """
         ProjectArchiveViewを表示したとき、Kawazメンバーはアーカイブ化されていて公開された全てのプロジェクトが見れる
        """

        for member in self.members:
            self.prefer_login(member)
            r = self.client.get('/projects/archives/')
            self.assertTemplateUsed(r, 'projects/project_archive.html')
            object_list = r.context['object_list']
            self.assertEqual(len(object_list), 2)

    def test_not_members_can_view_public_archive(self):
        """
        ProjectArchiveViewを表示したとき、メンバー以外はアーカイブ化されていてpublicなプロジェクトのみが見れる
        """
        for member in self.non_members:
            self.prefer_login(member)
            r = self.client.get('/projects/archives/')
            self.assertTemplateUsed(r, 'projects/project_archive.html')
            object_list = r.context['object_list']
            self.assertEqual(len(object_list), 1)

    def test_context_has_paginator(self):
        """
        ProjectArchiveViewのcontextにpaginatorが含まれている
        """
        r = self.client.get('/projects/archives/')
        self.assertTemplateUsed(r, 'projects/project_archive.html')
        self.assertTrue('page_obj' in r.context)
        self.assertTrue('paginator' in r.context)

    def test_paginate_by(self):
        """
        ProjectArchiveViewでは1ページに50個までしかProjectが含まれない
        また、ページネーションができていて、次のページには残りのオブジェクトが含まれている
        """
        for i in range(70):
            ProjectFactory(status='eternal')
        r = self.client.get('/projects/archives/')
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 50)

        r = self.client.get('/projects/archives/?page=2')
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 21)

    def test_order_by(self):
        """
         ProjectArchiveViewにoパラメータを渡すとstatus, created_at, title, categoryについてソートできる
        """
        self.prefer_login(self.members[0])
        p0 = ProjectFactory(status='paused')
        p1 = ProjectFactory(status='done')

        def _order_by(order_by):
            r = self.client.get('/projects/archives/', {'o': order_by})
            object_list = r.context['object_list']
            archives = Project.objects.archived(self.members[0]).order_by(order_by)
            for i in range(len(object_list)):
                self.assertEqual(object_list[i], archives[i])

        _order_by('status')
        _order_by('created_at')
        _order_by('title')
        _order_by('category')



class ProjectJoinViewTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_cannnot_join_project(self):
        '''
        Tests anonymous users attempt to access to ProjectJoinViewTestCase with GET method,
        redirects to Login page.
        '''
        r = self.client.get('/projects/1/join/')
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, '/projects/1/join/'))

    def test_get_method_is_not_allowed(self):
        '''
        Tests authorized attempt to access to ProjectJoinViewTestCase with GET method,
        it returns 405
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/projects/1/join/')
        self.assertEqual(r.status_code, 405)

    def test_user_can_join_project_via_project_join_view(self):
        '''
        Tests user can join to project via ProjectJoinView
        then redirects to project permalinks
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/projects/1/join/')
        self.assertRedirects(r, '/projects/{}/'.format(self.project.slug))
        self.assertEqual(self.project.members.count(), 2)
        self.assertTrue(self.user in self.project.members.all())


class ProjectQuitViewTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_cannnot_quit_project(self):
        '''
        Tests anonymous users attempt to access to ProjectQuitViewTestCase with GET method,
        redirects to Login page.
        '''
        r = self.client.get('/projects/1/quit/')
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, '/projects/1/quit/'))

    def test_get_method_is_not_allowed(self):
        '''
        Tests authorized attempt to access to ProjectQuitViewTestCase with GET method,
        it returns 405
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        self.project.join(self.user)
        r = self.client.get('/projects/1/quit/')
        self.assertEqual(r.status_code, 405)

    def test_user_can_quit_project_via_project_quit_view(self):
        '''
        Tests user can quit from project via ProjectQuitView
        then redirects to project permalinks
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        self.project.join(self.user)
        self.assertEqual(self.project.members.count(), 2)
        self.assertTrue(self.project.members.all())
        r = self.client.post('/projects/1/quit/')
        self.assertRedirects(r, '/projects/{}/'.format(self.project.slug))
        self.assertEqual(self.project.members.count(), 1)
        self.assertFalse(self.user in self.project.members.all())


class ProjectPreviewTestCase(TestCase):
    def test_project_preview(self):
        """
        /projects/preview/にアクセスできます
        """
        import json
        r = self.client.post('/projects/preview/', json.dumps({}), content_type='application/json')
        self.assertTemplateUsed(r, 'projects/components/project_detail.html')

    def test_reverse_preview(self):
        """
        projects_project_previewが引けます
        """
        self.assertEqual(reverse('projects_project_preview'), '/projects/preview/')
