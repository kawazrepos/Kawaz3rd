from django.test import TestCase
from django.template.loader import render_to_string
from ...extras.youtube import parse_youtube_urls


class ParseYouTubeURLsTestCase(TestCase):
    def setUp(self):
        self.video_id = 'r-j9FZ2TQd0'
        self.template_str = 'https://www.youtube.com/watch?v={}'
        self.width = 640
        self.height = 360

    def _render_template(self, video_id,
                         responsive=False, width=None, height=None):
        return render_to_string('kfm/extras/youtube.html', {
            'video_id': video_id,
            'responsive': responsive,
            'width': width or self.width,
            'height': height or self.height,
        }).strip()

    def test_parse_youtube_urls(self):
        """YouTubeのURLは展開される"""
        value = self.template_str.format(self.video_id)
        value = parse_youtube_urls(value)
        self.assertEqual(value, self._render_template(self.video_id))

    def test_parse_shorten_youtube_urls(self):
        """短縮されたYouTubeのURLは展開される"""
        value = "https://youtu.be/{}".format(self.video_id)
        value = parse_youtube_urls(value)
        self.assertEqual(value, self._render_template(self.video_id))

    def test_parse_youtube_urls_responsive(self):
        """YouTubeのURLはレスポンシブ展開される"""
        value = self.template_str.format(self.video_id)
        value = parse_youtube_urls(value, responsive=True)
        self.assertEqual(value, self._render_template(
            self.video_id,
            responsive=True,
        ))

    def test_parse_youtube_urls_width(self):
        """YouTubeのURLは展開される (Width指定)"""
        value = self.template_str.format(self.video_id)
        value = parse_youtube_urls(value, width=100)
        self.assertEqual(value, self._render_template(
            self.video_id,
            width=100,
            height=56,  # アスペクト比16:9に自動指定される
        ))

    def test_parse_youtube_urls_height(self):
        """YouTubeのURLは展開される (Height指定)"""
        value = self.template_str.format(self.video_id)
        value = parse_youtube_urls(value, height=100)
        self.assertEqual(value, self._render_template(
            self.video_id,
            height=100,
        ))

    def test_parse_youtube_urls_single_quoated(self):
        """シングルクォートされたYouTubeURLは展開されない"""
        template_str = "'{}'".format(self.template_str)
        original = template_str.format(self.video_id)
        value = parse_youtube_urls(original)
        self.assertEqual(value, original)

    def test_parse_youtube_urls_double_quoated(self):
        """ダブルクォートされたYouTubeURLは展開されない"""
        template_str = "\"{}\"".format(self.template_str)
        original = template_str.format(self.video_id)
        value = parse_youtube_urls(original)
        self.assertEqual(value, original)

    def test_parse_youtube_urls_fenced(self):
        """フェンス化されたYouTubeURLは展開されない"""
        template_str = "`{}`".format(self.template_str)
        original = template_str.format(self.video_id)
        value = parse_youtube_urls(original)
        self.assertEqual(value, original)

        template_str = "```\n{}\n```".format(self.template_str)
        original = template_str.format(self.video_id)
        value = parse_youtube_urls(original)
        self.assertEqual(value, original)

    def test_parse_youtube_urls_multiple(self):
        """複数のYouTubeURLも正しく展開される"""
        template_str = (
            "オススメ動画です\n"
            "http://www.youtube.com/watch?v={}\n"
            "しつこいですがオススメです\n"
            "http://www.youtube.com/watch?v={}\n"
            "オススメ http://www.youtube.com/watch?v={}\n"
            "http://www.youtube.com/watch?v={} かなり\n"
        )
        value = template_str.format(
            self.video_id, self.video_id,
            self.video_id, self.video_id,
        )
        value = parse_youtube_urls(value)
        self.assertEqual(value, (
            "オススメ動画です\n"
            "{}\n"
            "しつこいですがオススメです\n"
            "{}\n"
            "オススメ {}\n"
            "{} かなり\n"
        ).format(
            self._render_template(self.video_id),
            self._render_template(self.video_id),
            self._render_template(self.video_id),
            self._render_template(self.video_id),
        ))


