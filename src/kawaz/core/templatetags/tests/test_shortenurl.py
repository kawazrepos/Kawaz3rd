from unittest.mock import MagicMock, patch
from django.test import TestCase, override_settings
from django.template import Template, Context


URL = "http://www.kawaz.org"

@override_settings(GOOGLE_URL_SHORTENER_API_KEY='key')
class ShortenURLTestCase(TestCase):
    def test_shortenurl_templatetag(self):
        t = Template((
            "{% load shortenurl %}"
            "{% shortenurl %}"
            "かわずたんが「けろ〜ん」を書きました http://www.kawaz.org/blogs/hoge/"
            "{% endshortenurl %}"
        ))

        with patch('kawaz.core.utils.shortenurl.shorten') as shorten:
            shorten.return_value = 'http://goo.gl/testurl'
            rendered = t.render(Context())
        self.assertRegex(rendered, r'http:\/\/goo\.gl\/.+')
