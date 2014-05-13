from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import AnnouncementFactory

class AnnouncementAddPermissionTestCase(TestCase):
    def setUp(self):
        self.nerv = PersonaFactory(role='nerv')
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_staffs_have_add_announcement_permission(self):
        '''
        Tests staffs have permission to add announcements
        '''
        self.assertTrue(self.nerv.has_perm('announcements.add_announcement'))

    def test_users_dont_have_add_announcement_permission(self):
        '''
        Tests users do not have permission to add announcements
        '''
        self.assertFalse(self.user.has_perm('announcements.add_announcement'))

    def test_wille_dont_have_add_announcement_permission(self):
        '''
        Tests wille users do not have permission to add announcements
        '''
        self.assertFalse(self.wille.has_perm('announcements.add_announcement'))

    def test_anonymous_dont_have_add_announcement_permission(self):
        '''
        Tests anonymous users do not have permission to add announcements
        '''
        self.assertFalse(self.anonymous.has_perm('announcements.add_announcement'))


class AnnouncementChangePermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.nerv = PersonaFactory(role='nerv')
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()
        self.announcement = AnnouncementFactory()

    def test_staffs_have_change_announcement_permission(self):
        '''
        Tests staffs have permission to change announcements
        '''
        self.assertTrue(self.nerv.has_perm('announcements.change_announcement'))

    def test_users_dont_have_change_announcement_permission(self):
        '''
        Tests users do not have permission to change announcements
        '''
        self.assertFalse(self.user.has_perm('announcements.change_announcement'))

    def test_wille_dont_have_change_announcement_permission(self):
        '''
        Tests wille users do not have permission to change announcements
        '''
        self.assertFalse(self.wille.has_perm('announcements.change_announcement'))

    def test_anonymous_dont_have_change_announcement_permission(self):
        '''
        Tests anonymous users do not have permission to change announcements
        '''
        self.assertFalse(self.anonymous.has_perm('announcements.change_announcement'))

    def test_staffs_have_change_announcement_permission_with_object(self):
        '''
        Tests staffs have permission to change specific announcement
        '''
        self.assertTrue(self.nerv.has_perm('announcements.change_announcement', obj=self.announcement))

    def test_users_dont_have_change_announcement_permission_with_object(self):
        '''
        Tests users do not have permission to change specific announcement
        '''
        self.assertFalse(self.user.has_perm('announcements.change_announcement', obj=self.announcement))

    def test_author_have_change_permission(self):
        '''
        Tests onwers have permission to change own announcement
        '''
        self.assertTrue(self.announcement.author.has_perm('announcements.change_announcement', obj=self.announcement))

    def test_wille_dont_have_change_announcement_permission_with_object(self):
        '''
        Tests wille users do not have permission to change specific announcement
        '''
        self.assertFalse(self.wille.has_perm('announcements.change_announcement', obj=self.announcement))

    def test_anonymous_dont_have_change_announcement_permission_with_object(self):
        '''
        Tests anonymous users do not have permission to change specific announcement
        '''
        self.assertFalse(self.anonymous.has_perm('announcements.change_announcement', obj=self.announcement))


class AnnouncementDeletePermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.nerv = PersonaFactory(role='nerv')
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()
        self.announcement = AnnouncementFactory()

    def test_staffs_have_delete_announcement_permission(self):
        '''
        Tests staffs have permission to delete announcements
        '''
        self.assertTrue(self.nerv.has_perm('announcements.delete_announcement'))

    def test_users_do_not_have_delete_announcement_permission(self):
        '''
        Tests users do not have permission to delete announcements
        '''
        self.assertFalse(self.user.has_perm('announcements.delete_announcement'))

    def test_wille_dont_have_delete_announcement_permission(self):
        '''
        Tests wille users do not have permission to delete announcements
        '''
        self.assertFalse(self.wille.has_perm('announcements.delete_announcement'))

    def test_anonymous_dont_have_delete_announcement_permission(self):
        '''
        Tests anonymous users do not have permission to delete announcements
        '''
        self.assertFalse(self.anonymous.has_perm('announcements.delete_announcement'))

    def test_staffs_have_delete_announcement_permission_with_object(self):
        '''
        Tests users have permission to delete specific announcement
        '''
        self.assertTrue(self.nerv.has_perm('announcements.delete_announcement', obj=self.announcement))

    def test_users_dont_have_delete_announcement_permission_with_object(self):
        '''
        Tests users do not have permission to delete specific announcement
        '''
        self.assertFalse(self.user.has_perm('announcements.delete_announcement', obj=self.announcement))

    def test_author_have_delete_permission(self):
        '''
        Tests onwers have permission to delete own announcement
        '''
        self.assertTrue(self.announcement.author.has_perm('announcements.delete_announcement', obj=self.announcement))

    def test_wille_dont_have_delete_announcement_permission_with_object(self):
        '''
        Tests wille users do not have permission to delete specific announcement
        '''
        self.assertFalse(self.wille.has_perm('announcements.delete_announcement', obj=self.announcement))

    def test_anonymous_dont_have_delete_announcement_permission_with_object(self):
        '''
        Tests anonymous users do not have permission to delete specific announcement
        '''
        self.assertFalse(self.anonymous.has_perm('announcements.delete_announcement', obj=self.announcement))
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()
        self.announcement = AnnouncementFactory()
