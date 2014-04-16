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

        staff = PersonaFactory(is_staff=True)
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
