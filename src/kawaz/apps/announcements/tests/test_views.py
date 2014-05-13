import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from .factories import AnnouncementFactory
from ..models import Announcement
from kawaz.core.personas.tests.factories import PersonaFactory

class AnnouncementDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.nerv = PersonaFactory(role='nerv')
        self.nerv.set_password('password')
        self.nerv.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_view_public_announcement(self):
        '''Tests anonymous user can view public announcement'''
        announcement = AnnouncementFactory()
        r = self.client.get(announcement.get_absolute_url())
        self.assertTemplateUsed(r, 'announcements/announcement_detail.html')
        self.assertEqual(r.context_data['object'], announcement)

    def test_authorized_user_can_view_public_announcement(self):
        '''Tests authorized user can view public announcement'''
        announcement = AnnouncementFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(announcement.get_absolute_url())
        self.assertTemplateUsed(r, 'announcements/announcement_detail.html')
        self.assertEqual(r.context_data['object'], announcement)

    def test_anonymous_user_can_not_view_protected_announcement(self):
        '''Tests anonymous user can not view protected announcement'''
        announcement = AnnouncementFactory(pub_state='protected')
        r = self.client.get(announcement.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, announcement.get_absolute_url()))

    def test_authorized_user_can_view_protected_announcement(self):
        '''Tests authorized user can view public announcement'''
        announcement = AnnouncementFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(announcement.get_absolute_url())
        self.assertTemplateUsed(r, 'announcements/announcement_detail.html')
        self.assertEqual(r.context_data['object'], announcement)

    def test_wille_user_can_not_view_protected_announcement(self):
        '''
        Tests wille user can not view any protected announcements
        '''
        announcement = AnnouncementFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get(announcement.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, announcement.get_absolute_url()))


    def test_anonymous_user_can_not_view_draft_announcement(self):
        '''Tests anonymous user can not view draft announcement'''
        announcement = AnnouncementFactory(pub_state='draft')
        r = self.client.get(announcement.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, announcement.get_absolute_url()))


    def test_others_can_not_view_draft_announcement(self):
        '''
        Tests others can not view draft announcement
        User will redirect to '/announcements/1/update/'
        '''
        announcement = AnnouncementFactory(pub_state='draft')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(announcement.get_absolute_url())
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/{}/update/'.format(announcement.pk))

    def test_author_can_view_draft_announcement(self):
        '''Tests author can view draft announcement on update view'''
        announcement = AnnouncementFactory(pub_state='draft', author=self.nerv)
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.get(announcement.get_absolute_url())
        self.assertTemplateUsed(r, 'announcements/announcement_form.html')
        self.assertEqual(r.context_data['object'], announcement)

class AnnouncementCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.nerv = PersonaFactory(role='nerv')
        self.nerv.set_password('password')
        self.nerv.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_not_create_view(self):
        '''Tests anonymous user can not view AnnouncementCreateView'''
        r = self.client.get('/announcements/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/create/')

    def test_wille_user_can_not_view_announcement_create_view(self):
        '''Tests wille user can not view AnnouncementCreateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/announcements/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/create/')

    def test_general_user_can_not_view_announcement_create_view(self):
        '''Tests general user can not view AnnouncementCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/announcements/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/create/')

    def test_staff_user_can_view_announcement_create_view(self):
        '''Tests staff user can view AnnouncementCreateView'''
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.get('/announcements/create/')
        self.assertTemplateUsed(r, 'announcements/announcement_form.html')
        self.assertFalse('object' in r.context_data)

    def test_anonymous_user_can_not_create_via_create_view(self):
        '''Tests anonymous user can not create announcement via AnnouncementCreateView'''
        r = self.client.post('/announcements/create/', {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/create/')

    def test_wille_user_can_not_create_via_create_view(self):
        '''Tests wille user can not create announcement via AnnouncementCreateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/announcements/create/', {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/create/')


    def test_staff_user_can_create_via_create_view(self):
        '''Tests staff user can create announcement via AnnouncementCreateView'''
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.post('/announcements/create/', {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True
        })
        self.assertRedirects(r, '/announcements/1/')
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.get(pk=1)
        self.assertEqual(e.title, '【悲報】データ消えました')

    def test_authorized_user_can_create_via_create_view(self):
        '''Tests authorized user can create announcement via AnnouncementCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/announcements/create/', {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/create/')

    def test_staffs_cannot_modify_author_id(self):
        '''
        Tests authorized user cannot modify author id.
        In announcement creation form, `author` is exist as hidden field.
        So user can modify `author` to invalid values.
        This test checks that `author` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.post('/announcements/create/', {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True,
            'author' : other.pk
        })
        self.assertRedirects(r, '/announcements/1/')
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.get(pk=1)
        self.assertEqual(e.author, self.nerv)
        self.assertNotEqual(e.author, other)


class AnnouncementUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='author_kawaztan')
        self.user.set_password('password')
        self.other = PersonaFactory(username='black_kawaztan')
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.announcement = AnnouncementFactory(title='かわずたんのゲームだよ☆', author=self.user)
        self.category = CategoryFactory()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_not_view_announcement_update_view(self):
        '''Tests anonymous user can not view AnnouncementUpdateView'''
        r = self.client.get('/announcements/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/1/update/')

    def test_wille_user_can_not_view_announcement_update_view(self):
        '''Tests wille user can not view AnnouncementUpdateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/announcements/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/1/update/')

    def test_authorized_user_can_view_announcement_update_view(self):
        '''
        Tests authorized user can view AnnouncementUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/announcements/1/update/')
        self.assertTemplateUsed(r, 'announcements/announcement_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.announcement)

    def test_member_can_view_announcement_update_view(self):
        '''
        Tests announcement members can view AnnouncementUpdateView
        '''
        self.announcement.join(self.other)
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.get('/announcements/1/update/')
        self.assertTemplateUsed(r, 'announcements/announcement_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.announcement)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update announcement via AnnouncementUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/announcements/1/update/', {
            'pub_state' : 'public',
            'title' : 'クラッカーだよー',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/1/update/')
        self.assertEqual(self.announcement.title, 'かわずたんのゲームだよ☆')

    def test_wille_user_can_not_update_via_update_view(self):
        '''
        Tests wille user can not update announcement via AnnouncementUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/announcements/1/update/', {
            'pub_state' : 'public',
            'title' : '外部ユーザーだよーん',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/1/update/')
        self.assertEqual(self.announcement.title, 'かわずたんのゲームだよ☆')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update announcement via AnnouncementUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/announcements/1/update/', {
            'pub_state' : 'public',
            'title' : 'いたずら日記です',
            'body' : '黒かわずたんだよーん',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/1/update/')
        self.assertEqual(self.announcement.title, 'かわずたんのゲームだよ☆')

    def test_author_can_update_via_update_view(self):
        '''Tests author user can update announcement via AnnouncementUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/announcements/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.slug))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')

    def test_member_can_update_via_update_view(self):
        '''Tests announcement member can update announcement via AnnouncementUpdateView'''
        self.announcement.join(self.other)
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/announcements/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.slug))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')

    def test_user_cannot_update_slug(self):
        '''Tests anyone cannot update prject's slug'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        old_slug = self.announcement.slug
        r = self.client.post('/announcements/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk,
            'slug' : 'new-slug'
        })
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.slug))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.get(pk=1)
        self.assertEqual(e.slug, old_slug)
        self.assertNotEqual(e.slug, 'new-slug')

    def test_user_cannot_modify_author_id(self):
        '''
        Tests authorized user cannot modify author id.
        In announcement update form, `author` is exist as hidden field.
        So user can modify `author` to invalid values.
        This test checks that `author` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/announcements/1/update/', {
            'pub_state' : 'public',
            'title' : 'ID書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk,
            'author' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.slug))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.get(pk=1)
        self.assertEqual(e.author, self.user)
        self.assertNotEqual(e.author, other)
        self.assertEqual(e.title, 'ID書き換えます！')

class AnnouncementDeleteViewTestCase(TestCase):
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
        self.announcement = AnnouncementFactory(author=self.user)

    def test_author_can_delete_via_announcement_delete_view(self):
        '''
        Tests authors can delete its own announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/announcements/1/delete/', {})
        self.assertEqual(Announcement.objects.count(), 0)

    def test_member_cannot_delete_via_announcement_delete_view(self):
        '''
        Tests members cannot delete its announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        self.announcement.join(self.other)
        r = self.client.post('/announcements/1/delete/', {})
        self.assertEqual(Announcement.objects.count(), 1)

    def test_other_cannot_delete_via_announcement_delete_view(self):
        '''
        Tests others cannot delete announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/announcements/1/delete/', {})
        self.assertEqual(Announcement.objects.count(), 1)

    def test_wille_cannot_delete_via_announcement_delete_view(self):
        '''
        Tests wille cannot delete announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/announcements/1/delete/', {})
        self.assertEqual(Announcement.objects.count(), 1)

    def test_anonymous_cannot_delete_via_announcement_delete_view(self):
        '''
        Tests anonymous cannot delete announcements via AnnouncementDeleteView
        '''
        r = self.client.post('/announcements/1/delete/', {})
        self.assertEqual(Announcement.objects.count(), 1)


class AnnouncementListViewTestCase(TestCase):
    def setUp(self):
        self.announcements = (
            AnnouncementFactory(),
            AnnouncementFactory(pub_state='protected'),
            AnnouncementFactory(pub_state='draft'),
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_can_view_only_public_announcements(self):
        '''
        Tests anonymous user can view public Announcement only.
        The protected announcements are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/announcements/')
        self.assertTemplateUsed('announcements/announcement_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one announcement')
        self.assertEqual(list[0], self.announcements[0])

    def test_wille_can_view_only_public_announcements(self):
        '''
        Tests wille user can view public Announcement only.
        The protected announcements are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/announcements/')
        self.assertTemplateUsed('announcements/announcement_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one announcement')
        self.assertEqual(list[0], self.announcements[0])

    def test_authenticated_can_view_all_publish_announcements(self):
        '''
        Tests authenticated user can view all published announcements.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/announcements/')
        self.assertTemplateUsed('announcements/announcement_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two announcements')
        self.assertEqual(list[0], self.announcements[1], 'protected')
        self.assertEqual(list[1], self.announcements[0], 'public')


class AnnouncementJoinViewTestCase(TestCase):
    def setUp(self):
        self.announcement = AnnouncementFactory()
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_cannnot_join_announcement(self):
        '''
        Tests anonymous users attempt to access to AnnouncementJoinViewTestCase with GET method,
        redirects to Login page.
        '''
        r = self.client.get('/announcements/1/join/')
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, '/announcements/1/join/'))

    def test_get_method_is_not_allowed(self):
        '''
        Tests authorized attempt to access to AnnouncementJoinViewTestCase with GET method,
        it returns 405
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/announcements/1/join/')
        self.assertEqual(r.status_code, 405)

    def test_user_can_join_announcement_via_announcement_join_view(self):
        '''
        Tests user can join to announcement via AnnouncementJoinView
        then redirects to announcement permalinks
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/announcements/1/join/')
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.slug))
        self.assertEqual(self.announcement.members.count(), 2)
        self.assertTrue(self.user in self.announcement.members.all())


class AnnouncementQuitViewTestCase(TestCase):
    def setUp(self):
        self.announcement = AnnouncementFactory()
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_cannnot_quit_announcement(self):
        '''
        Tests anonymous users attempt to access to AnnouncementQuitViewTestCase with GET method,
        redirects to Login page.
        '''
        r = self.client.get('/announcements/1/quit/')
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, '/announcements/1/quit/'))

    def test_get_method_is_not_allowed(self):
        '''
        Tests authorized attempt to access to AnnouncementQuitViewTestCase with GET method,
        it returns 405
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        self.announcement.join(self.user)
        r = self.client.get('/announcements/1/quit/')
        self.assertEqual(r.status_code, 405)

    def test_user_can_quit_announcement_via_announcement_quit_view(self):
        '''
        Tests user can quit from announcement via AnnouncementQuitView
        then redirects to announcement permalinks
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        self.announcement.join(self.user)
        self.assertEqual(self.announcement.members.count(), 2)
        self.assertTrue(self.announcement.members.all())
        r = self.client.post('/announcements/1/quit/')
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.slug))
        self.assertEqual(self.announcement.members.count(), 1)
        self.assertFalse(self.user in self.announcement.members.all())
