from itertools import chain
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from .factories import AnnouncementFactory
from kawaz.apps.announcements.views import AnnouncementListView
from ..models import Announcement
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

    def prefer_login(self, user):
        if user.is_authenticated():
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))


class AnnouncementDetailViewTestCase(ViewTestCaseBase):
    template_path = 'announcements/announcement_detail.html'

    def test_reverse_url(self):
        """
        AnnouncementDetailViewの逆引き
        """
        announcement = AnnouncementFactory()
        self.assertEqual(
            reverse('announcements_announcement_detail', kwargs=dict(
                pk=announcement.pk,
            )),
            '/announcements/{}/'.format(announcement.pk),
        )

    def test_everyone_can_view_public_announcement(self):
        """全員公開お知らせを見れる"""
        announcement = AnnouncementFactory()
        for user in chain(self.non_members, self.members):
            self.prefer_login(user)
            r = self.client.get(announcement.get_absolute_url())
            self.assertTemplateUsed(r, self.template_path)
            self.assertEqual(r.context_data['object'], announcement)

    def test_non_members_cannot_view_protected_announcement(self):
        """非メンバーは内部公開お知らせを見れない"""
        announcement = AnnouncementFactory(pub_state='protected')
        url = announcement.get_absolute_url()
        login_url = "{}?next={}".format(
            settings.LOGIN_URL, url,
        )
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertRedirects(r, login_url)

    def test_members_can_view_protected_announcement(self):
        """メンバーは内部公開お知らせを観れる"""
        announcement = AnnouncementFactory(pub_state='protected')
        url = announcement.get_absolute_url()
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertTemplateUsed(r, self.template_path)
            self.assertEqual(r.context_data['object'], announcement)

    def test_non_members_cannot_view_draft_announcement(self):
        """非メンバーは下書きお知らせを見れない"""
        announcement = AnnouncementFactory(pub_state='draft')
        url = announcement.get_absolute_url()
        login_url = "{}?next={}".format(
            settings.LOGIN_URL, url,
        )
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertRedirects(r, login_url)

    def test_members_cannot_view_draft_announcement(self):
        """メンバーは下書きお知らせを見れない"""
        announcement = AnnouncementFactory(pub_state='draft')
        url = announcement.get_absolute_url()
        login_url = "{}?next={}".format(
            settings.LOGIN_URL, url,
        )
        for user in self.members[3:]:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertRedirects(r, login_url)

    def test_staffs_can_view_draft_announcement(self):
        """スタッフは下書きお知らせを見れる"""
        announcement = AnnouncementFactory(pub_state='draft')
        url = announcement.get_absolute_url()
        for user in self.members[:3]:
            self.prefer_login(user)
            r = self.client.get(url)
            # 直で編集画面が描画されるようになっている
            self.assertTemplateUsed(r, 'announcements/announcement_form.html')
            self.assertEqual(r.context_data['object'], announcement)


# TODO: ここより下のリファクタリングはまだ行っていない
class AnnouncementCreateViewTestCase(ViewTestCaseBase):
    template_path = 'announcements/announcement_form.html'

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

    def test_reverse_url(self):
        """
        AnnouncementCreateViewの逆引き
        """
        self.assertEqual(
            reverse('announcements_announcement_create'),
            '/announcements/create/',
        )

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
        announcement = Announcement.objects.last()
        self.assertRedirects(r, '/announcements/{}/'.format(announcement.pk))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.last()
        self.assertEqual(e.title, '【悲報】データ消えました')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

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

    def test_set_last_modifier_user(self):
        """
        お知らせを作成したときにlast_modifierとauthorがセットされる
        """
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.post('/announcements/create/', {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True
        })
        announcement = Announcement.objects.last()
        self.assertRedirects(r, '/announcements/{}/'.format(announcement.pk))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.last()
        self.assertEqual(e.author, self.nerv)
        self.assertEqual(e.last_modifier, self.nerv)

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
        announcement = Announcement.objects.last()
        self.assertRedirects(r, '/announcements/{}/'.format(announcement.pk))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.last()
        self.assertEqual(e.author, self.nerv)
        self.assertNotEqual(e.author, other)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")


class AnnouncementUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='author_kawaztan', role='nerv')
        self.user.set_password('password')
        self.other = PersonaFactory(username='black_kawaztan')
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.nerv = PersonaFactory(role='nerv', username='nerv_kawaztan')
        self.nerv.set_password('password')
        self.nerv.save()
        self.announcement = AnnouncementFactory(title='かわずたんのお知らせだよ☆', author=self.user)
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_not_view_announcement_update_view(self):
        '''Tests anonymous user can not view AnnouncementUpdateView'''
        r = self.client.get('/announcements/{}/update/'.format(self.announcement.pk))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/{}/update/'.format(self.announcement.pk))

    def test_wille_user_can_not_view_announcement_update_view(self):
        '''Tests wille user can not view AnnouncementUpdateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/announcements/{}/update/'.format(self.announcement.pk))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/{}/update/'.format(self.announcement.pk))

    def test_general_user_can_not_view_announcement_update_view(self):
        '''
        Tests general user can view AnnouncementUpdateView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.get('/announcements/{}/update/'.format(self.announcement.pk))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/{}/update/'.format(self.announcement.pk))

    def test_staff_can_view_announcement_update_view(self):
        '''
        Tests staff members can view AnnouncementUpdateView
        '''
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.get('/announcements/{}/update/'.format(self.announcement.pk))
        self.assertTemplateUsed(r, 'announcements/announcement_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.announcement)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update announcement via AnnouncementUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/announcements/{}/update/'.format(self.announcement.pk), {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True,
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/{}/update/'.format(self.announcement.pk))
        self.assertEqual(self.announcement.title, 'かわずたんのお知らせだよ☆')

    def test_wille_user_can_not_update_via_update_view(self):
        '''
        Tests wille user can not update announcement via AnnouncementUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/announcements/{}/update/'.format(self.announcement.pk), {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True,
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/{}/update/'.format(self.announcement.pk))
        self.assertEqual(self.announcement.title, 'かわずたんのお知らせだよ☆')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update announcement via AnnouncementUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/announcements/{}/update/'.format(self.announcement.pk), {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True,
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/announcements/{}/update/'.format(self.announcement.pk))
        self.assertEqual(self.announcement.title, 'かわずたんのお知らせだよ☆')

    def test_staff_can_update_via_update_view(self):
        '''Tests author user can update announcement via AnnouncementUpdateView'''
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.post('/announcements/{}/update/'.format(self.announcement.pk), {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True,
        })
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.pk))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.last()
        self.assertEqual(e.title, '【悲報】データ消えました')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_set_last_modifier_via_update_view(self):
        """
        お知らせを更新したとき、last_modifierがセットされる
        """
        previous_modifier = self.announcement.last_modifier
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.post('/announcements/{}/update/'.format(self.announcement.pk), {
            'pub_state' : 'public',
            'title' : '【悲報】データ消えました',
            'body' : 'サードインパクトだ！',
            'silently' : True,
        })
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.pk))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.last()
        self.assertEqual(e.last_modifier, self.nerv)
        self.assertNotEqual(e.last_modifier, previous_modifier)

    def test_user_cannot_modify_author_id(self):
        '''
        Tests authorized user cannot modify author id.
        In announcement update form, `author` is exist as hidden field.
        So user can modify `author` to invalid values.
        This test checks that `author` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.post('/announcements/{}/update/'.format(self.announcement.pk), {
            'pub_state' : 'public',
            'title' : 'ID書き換えます！',
            'body' : 'サードインパクトだ！',
            'silently' : True,
            'author' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/announcements/{}/'.format(self.announcement.pk))
        self.assertEqual(Announcement.objects.count(), 1)
        e = Announcement.objects.last()
        self.assertEqual(e.author, self.user)
        self.assertNotEqual(e.author, other)
        self.assertEqual(e.title, 'ID書き換えます！')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

class AnnouncementDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(role='nerv')
        self.user.set_password('password')
        self.user.save()
        self.nerv = PersonaFactory(role='nerv')
        self.nerv.set_password('password')
        self.nerv.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.other = PersonaFactory()
        self.other.set_password('password')
        self.other.save()
        self.announcement = AnnouncementFactory(author=self.user)

    def test_author_can_delete_via_announcement_delete_view(self):
        '''
        Tests author can delete its own announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/announcements/{}/delete/'.format(self.announcement.pk), {})
        self.assertRedirects(r, '/announcements/')
        self.assertEqual(Announcement.objects.count(), 0)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_staff_can_delete_via_announcement_delete_view(self):
        '''
        Tests members can delete its announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.nerv, password='password'))
        r = self.client.post('/announcements/{}/delete/'.format(self.announcement.pk), {})
        self.assertRedirects(r, '/announcements/')
        self.assertEqual(Announcement.objects.count(), 0)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_other_cannot_delete_via_announcement_delete_view(self):
        '''
        Tests others cannot delete announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/announcements/{}/delete/'.format(self.announcement.pk), {})
        self.assertEqual(Announcement.objects.count(), 1)
        self.assertRedirects(r, '{0}?next=/announcements/{1}/delete/'.format(settings.LOGIN_URL, self.announcement.pk))

    def test_wille_cannot_delete_via_announcement_delete_view(self):
        '''
        Tests wille cannot delete announcements via AnnouncementDeleteView
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/announcements/{}/delete/'.format(self.announcement.pk), {})
        self.assertEqual(Announcement.objects.count(), 1)
        self.assertRedirects(r, '{0}?next=/announcements/{1}/delete/'.format(settings.LOGIN_URL, self.announcement.pk))

    def test_anonymous_cannot_delete_via_announcement_delete_view(self):
        '''
        Tests anonymous cannot delete announcements via AnnouncementDeleteView
        '''
        r = self.client.post('/announcements/{}/delete/'.format(self.announcement.pk), {})
        self.assertEqual(Announcement.objects.count(), 1)
        self.assertRedirects(r, '{0}?next=/announcements/{1}/delete/'.format(settings.LOGIN_URL, self.announcement.pk))


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
        self.assertTrue(self.announcements[1] in list)
        self.assertTrue(self.announcements[0] in list)

    def test_paginate_by(self):
        """
        paginator_byが5件にセットされている
        """
        self.assertEqual(AnnouncementListView.paginate_by, 5)
