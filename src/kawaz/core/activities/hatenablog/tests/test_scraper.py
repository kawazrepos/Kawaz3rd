import os
import pytz
import datetime
import requests
from unittest.mock import MagicMock, patch, PropertyMock
from django.test import TestCase
from ..models import HatenablogEntry
from ..scraper import HatenablogFeedScraper


def get(url, **kwargs):
    root = os.path.join(os.path.dirname(__file__), 'statics')
    load = lambda x: open(os.path.join(root, x), 'rb').read()
    response = MagicMock(spec=requests.Response)
    if url == 'feed_url':
        type(response).text = PropertyMock(return_value=load('feed.xml'))
    elif url == 'entry_url':
        type(response).text = PropertyMock(return_value=load('entry.html'))
    elif url == 'thumbnail_url':
        type(response).content = PropertyMock(return_value=load('thumbnail.png'))
    return response


@patch('kawaz.core.activities.hatenablog.scraper.requests.get', get)
class HatenablogFeedScraperTestCase(TestCase):
    def setUp(self):
        self.url = 'feed_url'
        self.scraper = HatenablogFeedScraper(url=self.url)

    def test_scraper_can_fetch_entries(self):
        qs = HatenablogEntry.objects.all()
        self.assertEqual(len(qs), 0)

        jst = pytz.timezone('Asia/Tokyo')

        self.scraper.fetch()
        qs = HatenablogEntry.objects.all()
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0].title, (
            "「ゲームコミュニティサミット2014」で「＊いどのなかにいる＊」"
            "というセッションをします")
        )
        self.assertEqual(qs[0].url, "entry_url")
        self.assertEqual(qs[0].created_at,
                         datetime.datetime(2014, 7, 2, 14, 1, 29, tzinfo=jst))
        self.assertEqual(qs[0].thumbnail,
                         ("thumbnails/activities/contrib/hatenablog"
                          "/thumbnail_url"))

    def test_scraper_does_not_fetch_duplicate(self):
        qs = HatenablogEntry.objects.all()
        self.assertEqual(len(qs), 0)

        self.scraper.fetch()
        qs = HatenablogEntry.objects.all()
        self.assertEqual(len(qs), 1)
        thumbnail = qs[0].thumbnail

        # 2回目実行しても1のまま
        self.scraper.fetch()
        qs = HatenablogEntry.objects.all()
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0].thumbnail, thumbnail)
