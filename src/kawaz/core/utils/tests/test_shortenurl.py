from django.test import TestCase
from kawaz.core.utils import shortenurl

__author__ = 'giginet'

URL = "http://www.kawaz.org"

class ShortenURLTestCase(TestCase):
    def test_shortenurl(self):
        """
        GoogleのURL短縮APIを使ってURLが短縮できる
        """
        url = shortenurl.shorten(URL)
        self.assertRegex(url, r'^http:\/\/goo.\gl\/.+$')

    def test_shortenurl_failed(self):
        """
         APIの実行が失敗したとき、元のURLを返す
        """
        def dummy_urlopen(request):
            raise Exception("")

        shortenurl.urllib.request.urlopen = dummy_urlopen
        url = shortenurl.shorten(URL)
        self.assertEqual(url, URL)
