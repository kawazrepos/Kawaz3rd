#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/9
#
__author__ = 'giginet'

from unittest.mock import MagicMock
from django.test import TestCase
from django.template import Template, Context

class BaseViewerTemplateTagTestCase(TestCase):

    def _test_template(self, before, after):
        c = Context({
            'body' : before
        })
        t = Template(
            """{%% load viewer %%}"""
            """{{ body | %(filter_name)s }}""" % {
                'filter_name': self.filter_name
            }
        )
        r = t.render(c)
        self.assertEqual(r.strip(), after.strip())

class YouTubeTemplateTagTestCase(BaseViewerTemplateTagTestCase):
    filter_name = 'youtube'

    def test_youtube(self):
        """
        YoutubeのURLからプレイヤーをembedします
        """
        body = r"""
オススメの動画です
https://www.youtube.com/watch?v=r-j9FZ2TQd0
        """
        expected = r"""
オススメの動画です
<iframe width="640" height="480" src="//www.youtube.com/embed/r-j9FZ2TQd0" frameborder="0" allowfullscreen></iframe>
        """
        self._test_template(body, expected)

    def test_youtube_multitimes(self):
        """
        YouTubeのURLが複数含まれたテキストを正しく展開します
        """
        body = r"""
オススメの動画です
https://www.youtube.com/watch?v=r-j9FZ2TQd0

ついでにこっちもおもしろいです
https://www.youtube.com/watch?v=LoH0dOyyGx8
        """.strip()
        expected = r"""
オススメの動画です
<iframe width="640" height="480" src="//www.youtube.com/embed/r-j9FZ2TQd0" frameborder="0" allowfullscreen></iframe>

ついでにこっちもおもしろいです
<iframe width="640" height="480" src="//www.youtube.com/embed/LoH0dOyyGx8" frameborder="0" allowfullscreen></iframe>
        """.strip()
        self._test_template(body, expected)

    def test_youtube_with_link(self):
        """
        YouTubeのURLがタグの中や文章に含まれてたら展開しません
        """
        body = r"""
        オススメの動画です
        <a href="https://www.youtube.com/watch?v=r-j9FZ2TQd0">オススメ</a>

        ついでにこっちもおもしろいですhttps://www.youtube.com/watch?v=LoH0dOyyGx8
        """.strip()
        expected = body
        self._test_template(body, expected)

