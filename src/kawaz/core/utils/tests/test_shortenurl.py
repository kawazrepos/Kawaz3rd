import json
from unittest.mock import MagicMock
from django.test import TestCase, override_settings
from kawaz.core.utils import shortenurl



URL = "http://www.kawaz.org"

@override_settings(GOOGLE_URL_SHORTENER_API_KEY='key')
class ShortenURLTestCase(TestCase):
    def test_shortenurl(self):
        """
        GoogleのURL短縮APIを使ってURLが短縮できる
        """
        def dummy_urlopen(request):
            mock = MagicMock()
            json_string = json.dumps({'id': 'http://goo.gl/hogehoge'})
            mock.read.return_value = json_string.encode('utf-8')
            return mock
        shortenurl.urlopen = dummy_urlopen

        url = shortenurl.shorten(URL)

        self.assertRegex(url, r'^http:\/\/goo.\gl\/.+$')

    def test_shortenurl_failed(self):
        """
         APIの実行が失敗したとき、元のURLを返す
        """
        def dummy_urlopen(request):
            raise Exception("Something went wrong")

        shortenurl.urlopen = dummy_urlopen
        url = shortenurl.shorten(URL)
        self.assertEqual(url, URL)
