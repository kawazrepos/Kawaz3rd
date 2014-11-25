from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import AnnouncementFactory


class AnnouncementViewPermissionTestCase(TestCase):

    def test_anybody_have_view_perm(self):
        """お知らせを見るモデル権限は全員が持つ"""
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.view_announcement'))
        user = PersonaFactory()
        self.assertTrue(user.has_perm('announcements.view_announcement'))
        user = AnonymousUser()
        self.assertTrue(user.has_perm('announcements.view_announcement'))

    def test_staff_has_view_perm_of_public(self):
        """スタッフは外部公開お知らせを見ることができる"""
        obj = AnnouncementFactory(pub_state='public')
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_authorized_has_view_perm_of_public(self):
        """ログインユーザーは外部公開お知らせを見ることができる"""
        obj = AnnouncementFactory(pub_state='public')
        user = PersonaFactory()
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_anonymous_has_view_perm_of_public(self):
        """非ログインユーザーは外部公開お知らせを見ることができる"""
        obj = AnnouncementFactory(pub_state='public')
        user = AnonymousUser()
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_staff_has_view_perm_of_protected(self):
        """スタッフは内部公開お知らせを見ることができる"""
        obj = AnnouncementFactory(pub_state='protected')
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_authorized_has_view_perm_of_protected(self):
        """ログインユーザーは公開お知らせを見ることができる"""
        obj = AnnouncementFactory(pub_state='protected')
        user = PersonaFactory()
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_anonymous_has_not_view_perm_of_protected(self):
        """非ログインユーザーは内部公開お知らせを見ることができない"""
        obj = AnnouncementFactory(pub_state='protected')
        user = AnonymousUser()
        self.assertFalse(user.has_perm('announcements.view_announcement', obj))

    def test_staff_has_view_perm_of_draft(self):
        """スタッフは下書きお知らせを見ることができる"""
        obj = AnnouncementFactory(pub_state='draft')
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_authorized_has_not_view_perm_of_draft(self):
        """ログインユーザ-は下書きお知らせを見ることができない"""
        obj = AnnouncementFactory(pub_state='draft')
        user = PersonaFactory()
        self.assertFalse(user.has_perm('announcements.view_announcement', obj))

    def test_anonymous_has_not_view_perm_of_draft(self):
        """非ログインユーザ-は下書きお知らせを見ることができない"""
        obj = AnnouncementFactory(pub_state='draft')
        user = AnonymousUser()
        self.assertFalse(user.has_perm('announcements.view_announcement', obj))


class AnnouncementAddPermissionTestCase(TestCase):
    def setUp(self):
        self.nerv = PersonaFactory(role='nerv')
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_staffs_have_add_announcement_perm(self):
        """
        スタッフはお知らせを作成する権限を持つ
        """
        self.assertTrue(self.nerv.has_perm(
            'announcements.add_announcement'))

    def test_users_dont_have_add_announcement_perm(self):
        """
        ログインユーザーはお知らせを作成する権限を持たない
        """
        self.assertFalse(self.user.has_perm(
            'announcements.add_announcement'))

    def test_wille_dont_have_add_announcement_perm(self):
        """
        Willeユーザーはお知らせを作成する権限を持たない
        """
        self.assertFalse(self.wille.has_perm(
            'announcements.add_announcement'))

    def test_anonymous_dont_have_add_announcement_perm(self):
        """
        非ログインユーザーはお知らせを作成する権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm(
            'announcements.add_announcement'))


class AnnouncementChangePermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.nerv = PersonaFactory(role='nerv')
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()
        self.announcement = AnnouncementFactory()

    def test_staffs_have_change_announcement_perm(self):
        """
        スタッフはお知らせ編集権限を持つ
        """
        self.assertTrue(self.nerv.has_perm(
            'announcements.change_announcement'))

    def test_users_dont_have_change_announcement_perm(self):
        """
        ログインユーザーはお知らせ編集権限を持たない
        """
        self.assertFalse(self.user.has_perm(
            'announcements.change_announcement'))

    def test_wille_dont_have_change_announcement_perm(self):
        """
        Willeユーザーはお知らせ編集権限を持たない
        """
        self.assertFalse(self.wille.has_perm(
            'announcements.change_announcement'))

    def test_anonymous_dont_have_change_announcement_perm(self):
        """
        非ログインユーザーはお知らせ編集権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm(
            'announcements.change_announcement'))

    def test_staffs_have_change_announcement_perm_with_obj(self):
        """
        スタッフはお知らせ編集権限を持つ（オブジェクト）
        """
        self.assertTrue(self.nerv.has_perm(
            'announcements.change_announcement', obj=self.announcement))

    def test_users_dont_have_change_announcement_perm_with_obj(self):
        """
        ログインユーザーはお知らせ編集権限を持たない（オブジェクト）
        """
        self.assertFalse(self.user.has_perm(
            'announcements.change_announcement', obj=self.announcement))

    def test_author_have_change_perm(self):
        """
        作成者はお知らせ編集権限を持つ（オブジェクト）
        """
        self.assertTrue(self.announcement.author.has_perm(
            'announcements.change_announcement', obj=self.announcement))

    def test_wille_dont_have_change_announcement_perm_with_obj(self):
        """
        Willeユーザーはお知らせ編集権限を持たない（オブジェクト）
        """
        self.assertFalse(self.wille.has_perm(
            'announcements.change_announcement', obj=self.announcement))

    def test_anonymous_dont_have_change_announcement_perm_with_obj(self):
        """
        非ログインユーザーはお知らせ編集権限を持たない（オブジェクト）
        """
        self.assertFalse(self.anonymous.has_perm(
            'announcements.change_announcement', obj=self.announcement))


class AnnouncementDeletePermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.nerv = PersonaFactory(role='nerv')
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()
        self.announcement = AnnouncementFactory()

    def test_staffs_have_delete_announcement_perm(self):
        """
        スタッフはお知らせ削除権限を持つ
        """
        self.assertTrue(self.nerv.has_perm(
            'announcements.delete_announcement'))

    def test_users_do_not_have_delete_announcement_perm(self):
        """
        ログインユーザーはお知らせ削除権限を持たない
        """
        self.assertFalse(self.user.has_perm(
            'announcements.delete_announcement'))

    def test_wille_dont_have_delete_announcement_perm(self):
        """
        Willeユーザーはお知らせ削除権限を持たない
        """
        self.assertFalse(self.wille.has_perm(
            'announcements.delete_announcement'))

    def test_anonymous_dont_have_delete_announcement_perm(self):
        """
        非ログインユーザーはお知らせ削除権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm(
            'announcements.delete_announcement'))

    def test_staffs_have_delete_announcement_perm_with_obj(self):
        """
        スタッフはお知らせ削除権限を持つ（オブジェクト）
        """
        self.assertTrue(self.nerv.has_perm(
            'announcements.delete_announcement', obj=self.announcement))

    def test_users_dont_have_delete_announcement_perm_with_obj(self):
        """
        ログインユーザーはお知らせ削除権限を持たない（オブジェクト）
        """
        self.assertFalse(self.user.has_perm(
            'announcements.delete_announcement', obj=self.announcement))

    def test_author_have_delete_perm(self):
        """
        作成者はお知らせ削除権限を持つ（オブジェクト）
        """
        self.assertTrue(self.announcement.author.has_perm(
            'announcements.delete_announcement', obj=self.announcement))

    def test_wille_dont_have_delete_announcement_perm_with_obj(self):
        """
        Willeユーザーはお知らせ削除権限を持たない（オブジェクト）
        """
        self.assertFalse(self.wille.has_perm(
            'announcements.delete_announcement', obj=self.announcement))

    def test_anonymous_dont_have_delete_announcement_perm_with_obj(self):
        """
        非ログインユーザーはお知らせ削除権限を持たない（オブジェクト）
        """
        self.assertFalse(self.anonymous.has_perm(
            'announcements.delete_announcement', obj=self.announcement))
