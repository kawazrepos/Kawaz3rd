from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Announcement
from .factories import AnnouncementFactory

class AnnouncementManagerTestCase(TestCase):
    def test_draft_by_staff(self):
        '''Tests draft returns correct queryset with staff'''
        AnnouncementFactory(pub_state='public')
        AnnouncementFactory(pub_state='protected')
        c = AnnouncementFactory(pub_state='draft')

        staff = PersonaFactory(role='nerv')
        qs = Announcement.objects.draft(staff)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], c)

    def test_draft_by_non_staff(self):
        '''Tests draft returns correct queryset with non staff'''
        AnnouncementFactory(pub_state='public')
        AnnouncementFactory(pub_state='protected')
        AnnouncementFactory(pub_state='draft')

        user = PersonaFactory()
        qs = Announcement.objects.draft(user)
        self.assertEqual(qs.count(), 0)

    def test_published_by_authorized(self):
        '''Tests published returns correct queryset with authorized'''
        a = AnnouncementFactory(pub_state='public')
        b = AnnouncementFactory(pub_state='protected')
        AnnouncementFactory(pub_state='draft')

        user = PersonaFactory()
        qs = Announcement.objects.published(user)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0], b)
        self.assertEqual(qs[1], a)

    def test_published_by_anonymous(self):
        '''Tests published returns correct queryset with anonymous'''
        a = AnnouncementFactory(pub_state='public')
        AnnouncementFactory(pub_state='protected')
        AnnouncementFactory(pub_state='draft')

        user = AnonymousUser()
        qs = Announcement.objects.published(user)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], a)

class AnnouncementTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        announcement = AnnouncementFactory(title='春のゲーム祭り開催のお知らせ')
        self.assertEqual(str(announcement), '春のゲーム祭り開催のお知らせ')

class AnnouncementEditPermissionTestCase(TestCase):

    def test_staff_has_add_perm(self):
        '''Tests staff can add announcement'''
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.add_announcement'))

    def test_authorized_has_not_add_perm(self):
        '''Tests authorized can not add announcement'''
        user = PersonaFactory()
        self.assertFalse(user.has_perm('announcements.add_announcement'))

    def test_anonymous_has_not_add_perm(self):
        '''Tests anonymous can not add announcement'''
        user = AnonymousUser()
        self.assertFalse(user.has_perm('announcements.add_announcement'))

    def test_staff_has_change_perm(self):
        '''Tests staff can change announcement'''
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.change_announcement'))

    def test_authorized_has_not_change_perm(self):
        '''Tests authorized can not change announcement'''
        user = PersonaFactory()
        self.assertFalse(user.has_perm('announcements.change_announcement'))

    def test_anonymous_has_not_change_perm(self):
        '''Tests anonymous can not change announcement'''
        user = AnonymousUser()
        self.assertFalse(user.has_perm('announcements.change_announcement'))

    def test_staff_has_delete_perm(self):
        '''Tests staff can delete announcement'''
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.delete_announcement'))

    def test_authorized_has_not_delete_perm(self):
        '''Tests authorized can not delete announcement'''
        user = PersonaFactory()
        self.assertFalse(user.has_perm('announcements.delete_announcement'))

    def test_anonymous_has_not_delete_perm(self):
        '''Tests anonymous can not delete announcement'''
        user = AnonymousUser()
        self.assertFalse(user.has_perm('announcements.delete_announcement'))

class AnnouncementViewPermissionTestCase(TestCase):

    def test_staff_has_view_perm_of_public(self):
        '''Tests staff can view public announcement'''
        obj = AnnouncementFactory(pub_state='public')
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_authorized_has_view_perm_of_public(self):
        '''Tests authorized can view public announcement'''
        obj = AnnouncementFactory(pub_state='public')
        user = PersonaFactory()
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_anonymous_has_view_perm_of_public(self):
        '''Tests anonymous can view public announcement'''
        obj = AnnouncementFactory(pub_state='public')
        user = AnonymousUser()
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_staff_has_view_perm_of_protected(self):
        '''Tests staff can view protected announcement'''
        obj = AnnouncementFactory(pub_state='protected')
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_authorized_has_view_perm_of_protected(self):
        '''Tests authorized can view protected announcement'''
        obj = AnnouncementFactory(pub_state='protected')
        user = PersonaFactory()
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_anonymous_has_not_view_perm_of_protected(self):
        '''Tests anonymous can not view protected announcement'''
        obj = AnnouncementFactory(pub_state='protected')
        user = AnonymousUser()
        self.assertFalse(user.has_perm('announcements.view_announcement', obj))

    def test_staff_has_view_perm_of_draft(self):
        '''Tests staff can view draft announcement'''
        obj = AnnouncementFactory(pub_state='draft')
        user = PersonaFactory(role='nerv')
        self.assertTrue(user.has_perm('announcements.view_announcement', obj))

    def test_authorized_has_not_view_perm_of_draft(self):
        '''Tests authorized can not view draft announcement'''
        obj = AnnouncementFactory(pub_state='draft')
        user = PersonaFactory()
        self.assertFalse(user.has_perm('announcements.view_announcement', obj))

    def test_anonymous_has_not_view_perm_of_draft(self):
        '''Tests anonymous can not view draft announcement'''
        obj = AnnouncementFactory(pub_state='draft')
        user = AnonymousUser()
        self.assertFalse(user.has_perm('announcements.view_announcement', obj))
