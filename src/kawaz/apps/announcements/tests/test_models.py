from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Announcement
from .factories import AnnouncementFactory


class AnnouncementManagerTestCase(TestCase):
    def test_draft_by_staff(self):
        """
        draftメソッドがスタッフに対し下書き状態の記事を含むQSを返す
        """
        '''Tests draft returns correct queryset with staff'''
        AnnouncementFactory(pub_state='public')
        AnnouncementFactory(pub_state='protected')
        c = AnnouncementFactory(pub_state='draft')

        staff = PersonaFactory(role='nerv')
        qs = Announcement.objects.draft(staff)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], c)

    def test_draft_by_non_staff(self):
        """
        draftメソッドが非スタッフに対し下書き状態の記事を含まないQSを返す
        """
        AnnouncementFactory(pub_state='public')
        AnnouncementFactory(pub_state='protected')
        AnnouncementFactory(pub_state='draft')

        user = PersonaFactory()
        qs = Announcement.objects.draft(user)
        self.assertEqual(qs.count(), 0)

    def test_published_by_authorized(self):
        """
        ログインユーザーに対しpublishedメソッドが内部公開の記事を含むQSを返す
        """
        a = AnnouncementFactory(pub_state='public')
        b = AnnouncementFactory(pub_state='protected')
        AnnouncementFactory(pub_state='draft')

        user = PersonaFactory()
        qs = Announcement.objects.published(user)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0], b)
        self.assertEqual(qs[1], a)

    def test_published_by_anonymous(self):
        """
        非ユーザーに対しpublishedメソッドが内部公開の記事を含まないQSを返す
        """
        a = AnnouncementFactory(pub_state='public')
        AnnouncementFactory(pub_state='protected')
        AnnouncementFactory(pub_state='draft')

        user = AnonymousUser()
        qs = Announcement.objects.published(user)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], a)

    def test_published_by_wille(self):
        """
        Willeユーザーに対しpublishedメソッドが内部公開の記事を含まないQSを返す
        """
        a = AnnouncementFactory(pub_state='public')
        AnnouncementFactory(pub_state='protected')
        AnnouncementFactory(pub_state='draft')

        user = PersonaFactory(role='wille')
        qs = Announcement.objects.published(user)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], a)


class AnnouncementTestCase(TestCase):
    def test_str(self):
        """str が正しい文字列を返す"""
        announcement = AnnouncementFactory(
            title='春のゲーム祭り開催のお知らせ'
        )
        self.assertEqual(str(announcement), '春のゲーム祭り開催のお知らせ')
