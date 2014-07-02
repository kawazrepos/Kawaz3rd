#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/2
#
import os
import datetime
from unittest import mock
from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings
from ..scraper import RecentActivityScraper
from .factories import RecentActivity

__author__ = 'giginet'

def static_file(url):
    """
    urllib.request.urlopenをstubして、特定の文字列が入ってきたときにfixture用のデータを返している
    """
    fixture_dir = os.path.join(settings.REPOSITORY_ROOT,
                               'src', 'kawaz', 'statics', 'fixtures', 'recent_activities')
    if url == 'feed_url':
        return open(os.path.join(fixture_dir, 'rss'), 'rb')
    elif url == "entry_url":
        return open(os.path.join(fixture_dir, 'entry'), 'rb')
    elif url == "thumbnail_url":
        return open(os.path.join(fixture_dir, 'thumbnail.png'), 'rb')
    else:
        raise Exception("argument {} is not allowed".format(url))

def patch_urllib_request_urlopen(mock_urlopen_function):
    """
    urllib.request.urlopenをpatchします
    """
    return mock.patch('urllib.request.urlopen', mock_urlopen_function)


@patch_urllib_request_urlopen(static_file)
@override_settings(RECENT_ACTIVITY_FEED_URL='feed_url')
class RecentActivityScraperTestCase(TestCase):
    def setUp(self):
        self.scraper = RecentActivityScraper(url=settings.RECENT_ACTIVITY_FEED_URL)

    def test_scraper_can_fetch_entries(self):
        """
        Scraper.fetch()でRecentActivityを取得できる
        """
        qs = RecentActivity.objects.all()
        self.assertEqual(len(qs), 0)

        self.scraper.fetch()
        qs = RecentActivity.objects.all()
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0].title, "「ゲームコミュニティサミット2014」で「＊いどのなかにいる＊」というセッションをします")
        self.assertEqual(qs[0].url, "entry_url")
        self.assertEqual(qs[0].publish_at, datetime.datetime(2014, 7, 1, 20, 1, 29))
        self.assertEqual(qs[0].thumbnail, "thumbnails/recent_activities/thumbnail_url")

    def test_scraper_cannot_fetch_duplicate(self):
        """
        Scraper.fetch()で同じRecentActivityが複数回取得されない
        """
        qs = RecentActivity.objects.all()
        self.assertEqual(len(qs), 0)

        self.scraper.fetch()
        qs = RecentActivity.objects.all()
        self.assertEqual(len(qs), 1)

        # 2回目実行しても1のまま
        self.scraper.fetch()
        qs = RecentActivity.objects.all()
        self.assertEqual(len(qs), 1)
