# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.template.loader import render_to_string
from ...extras.nicovideo import parse_nicovideo_urls


class ParseNicoVideoURLsTestCase(TestCase):
    def setUp(self):
        self.video_id = 'sm10805698'

    def _render_template(self, video_id):
        return render_to_string('kfm/extras/nicovideo.html', {
            'video_id': video_id,
        }).strip()

    def test_parse_nicovideo_urls(self):
        """ニコニコ動画のURLは展開される"""
        template_str = "http://www.nicovideo.jp/watch/{}"
        value = template_str.format(self.video_id)
        value = parse_nicovideo_urls(value)
        self.assertEqual(value, self._render_template(self.video_id))

    def test_parse_nicovideo_urls_single_quoated(self):
        """シングルクォートされたニコニコ動画URLは展開されない"""
        template_str = "'http://www.nicovideo.jp/watch/{}'"
        original = template_str.format(self.video_id)
        value = parse_nicovideo_urls(original)
        self.assertEqual(value, original)

    def test_parse_nicovideo_urls_double_quoated(self):
        """ダブルクォートされたニコニコ動画URLは展開されない"""
        template_str = "\"http://www.nicovideo.jp/watch/{}\""
        original = template_str.format(self.video_id)
        value = parse_nicovideo_urls(original)
        self.assertEqual(value, original)

    def test_parse_nicovideo_urls_fenced(self):
        """フェンス化されたニコニコ動画URLは展開されない"""
        template_str = "`http://www.nicovideo.jp/watch/{}`"
        original = template_str.format(self.video_id)
        value = parse_nicovideo_urls(original)
        self.assertEqual(value, original)

        template_str = "```\nhttp://www.nicovideo.jp/watch/{}\n```"
        original = template_str.format(self.video_id)
        value = parse_nicovideo_urls(original)
        self.assertEqual(value, original)

    def test_parse_nicovideo_urls_multiple(self):
        """複数のニコニコ動画URLも正しく展開される"""
        template_str = (
            "全てはここから始まった\n"
            "http://www.nicovideo.jp/watch/{}\n"
            "この動画がランキング上位になり知名度が爆発的に上がった\n"
            "http://www.nicovideo.jp/watch/{}\n"
            "オススメ http://www.nicovideo.jp/watch/{}\n"
            "http://www.nicovideo.jp/watch/{} かなり\n"
        )
        value = template_str.format(
            self.video_id, self.video_id,
            self.video_id, self.video_id,
        )
        value = parse_nicovideo_urls(value)
        self.assertEqual(value, (
            "全てはここから始まった\n"
            "{}\n"
            "この動画がランキング上位になり知名度が爆発的に上がった\n"
            "{}\n"
            "オススメ {}\n"
            "{} かなり\n"
        ).format(
            self._render_template(self.video_id),
            self._render_template(self.video_id),
            self._render_template(self.video_id),
            self._render_template(self.video_id),
        ))


