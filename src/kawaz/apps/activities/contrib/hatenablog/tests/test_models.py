import datetime
from django.utils import timezone
from django.test import TestCase
from .factories import HatenablogEntryFactory
from ..models import HatenablogEntry


class HatenablogEntryModelTestCase(TestCase):
    def test_str_returns_title(self):
        """
        str()関数はtitleの値を返す
        """
        hatenablog_entry = HatenablogEntryFactory(title='お知らせ')
        self.assertTrue(str(hatenablog_entry), 'お知らせ')

    def test_ordering(self):
        """
        HatenablogEntryは作成日順に並ぶ
        """
        standard_time = datetime.datetime(2014, 7, 1, tzinfo=timezone.utc)
        a0 = HatenablogEntryFactory(
            created_at=standard_time - datetime.timedelta(3))
        a1 = HatenablogEntryFactory(
            created_at=standard_time - datetime.timedelta(1))
        a2 = HatenablogEntryFactory(
            created_at=standard_time - datetime.timedelta(2))
        qs = HatenablogEntry.objects.all()
        self.assertEqual(len(qs), 3)
        self.assertEqual(qs[0], a1)
        self.assertEqual(qs[1], a2)
        self.assertEqual(qs[2], a0)
