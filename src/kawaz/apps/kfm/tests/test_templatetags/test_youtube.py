# coding=utf-8
"""
"""

from unittest.mock import patch
from django.test import TestCase
from django.template import Template, Context


class YouTubeTemplateTagTestCase(TestCase):
    def _test_template(self, body, farg=""):
        if farg:
            farg = ":"+farg
        t = Template((
            "{{% load youtube %}}"
            "{{{{ body | youtube{} }}}}"
        ).format(farg))
        return t.render(Context({'body': body}))

    @patch('kawaz.apps.kfm.templatetags.youtube.parse_youtube_urls')
    def test_youtube(self, parse_youtube_urls):
        """フィルタによりYouTube展開コードが呼び出される"""
        self._test_template("foobar")
        parse_youtube_urls.assert_called_with("foobar",
                                              responsive=False,
                                              width=None, height=None)

    @patch('kawaz.apps.kfm.templatetags.youtube.parse_youtube_urls')
    def test_youtube_responsive(self, parse_youtube_urls):
        """フィルタによりYouTube展開コードが呼び出される (responsive)"""
        self._test_template("foobar", farg="'responsive'")
        parse_youtube_urls.assert_called_with("foobar",
                                              responsive=True,
                                              width=None, height=None)

    @patch('kawaz.apps.kfm.templatetags.youtube.parse_youtube_urls')
    def test_youtube_width(self, parse_youtube_urls):
        """フィルタによりYouTube展開コードが呼び出される (width)"""
        self._test_template("foobar", farg="'100'")
        parse_youtube_urls.assert_called_with("foobar",
                                              responsive=False,
                                              width=100, height=None)

    @patch('kawaz.apps.kfm.templatetags.youtube.parse_youtube_urls')
    def test_youtube_width_and_height(self, parse_youtube_urls):
        """フィルタによりYouTube展開コードが呼び出される (width/height)"""
        self._test_template("foobar", farg="'100,200'")
        parse_youtube_urls.assert_called_with("foobar",
                                              responsive=False,
                                              width=100, height=200)

