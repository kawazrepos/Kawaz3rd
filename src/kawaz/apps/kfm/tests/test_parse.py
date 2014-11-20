# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.template import Template, Context
from django.template.loader import render_to_string
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.tests.factories import ProfileFactory
from kawaz.apps.attachments.tests.factories import MaterialFactory
from ..parser import parse_kfm


class ParseKFMTestCase(TestCase):

    def test_parse_kfm_multiple_underscore_in_words(self):
        """KFMは_や__によるem, strongを扱わない"""
        original = "_foo_ __bar__"
        value = parse_kfm(original)
        self.assertEqual(value, (
            "<p>_foo_ __bar__</p>"
        ))

    def test_parse_kfm_url_autolinking(self):
        """KFMはURLを自動展開する"""
        original = "http://www.kawaz.org/"
        value = parse_kfm(original)
        self.assertEqual(value, (
            "<p><a href=\"http://www.kawaz.org/\" rel=\"nofollow\">"
            "http://www.kawaz.org/"
            "</a></p>"
        ))

        original = "webmaster@kawaz.org"
        value = parse_kfm(original)
        self.assertEqual(value, (
            "<p><a href=\"mailto:webmaster@kawaz.org\">"
            "webmaster@kawaz.org"
            "</a></p>"
        ))


    def test_parse_kfm_strikethrough(self):
        """KFMは~~シンタックスを理解し<del>に変換する"""
        original = "~~DELETE~~"
        value = parse_kfm(original)
        self.assertEqual(value, (
            "<p><del>DELETE</del></p>"
        ))

    def test_parse_kfm_fenced_code_blocks(self):
        """KFMはコードブロックシンタックスを扱える"""
        original = "```\ncode block\n```"
        value = parse_kfm(original)
        self.assertEqual(value, (
            "<pre><code>code block\n</code></pre>"
        ))

    def test_parse_kfm_syntax_highlight(self):
        """KFMはシンタックスハイライトを扱える"""
        # Note: pygments がインストールされている必要がある
        original = "```python\nimport os\n```"
        value = parse_kfm(original)
        self.assertEqual(value, (
            "<div class=\"codehilite\"><pre><code>"
            "<span class=\"kn\">import</span> "
            "<span class=\"nn\">os</span>\n"
            "</code></pre></div>"
        ))

    def test_parse_kfm_table(self):
        """KFMはテーブルシンタックスを扱える"""
        original = (
            "| Header 1 | Header 2 |\n"
            "| -------- | -------- |\n"
            "| Cell 1   | Cell 2   |\n"
            "| Cell 3   | Cell 4   |\n"
        )
        value = parse_kfm(original)
        self.assertEqual(value, (
            "<table>\n"
            "<thead>\n"
            "<tr>\n"
            "  <th>Header 1</th>\n"
            "  <th>Header 2</th>\n"
            "</tr>\n"
            "</thead>\n"
            "<tbody>\n"
            "<tr>\n"
            "  <td>Cell 1</td>\n"
            "  <td>Cell 2</td>\n"
            "</tr>\n"
            "<tr>\n"
            "  <td>Cell 3</td>\n"
            "  <td>Cell 4</td>\n"
            "</tr>\n"
            "</tbody>\n"
            "</table>"
        ))

    def test_parse_kfm_footnote(self):
        """KFMは脚注シンタックスを扱える"""
        original = (
            "foobar [^note]\n"
            "[^note]: hoge\n"
        )
        value = parse_kfm(original)
        self.assertIn("footnote-ref", value)
        self.assertIn("class=\"footnotes\"", value)

    def test_parse_kfm_cuddled_lists(self):
        """KFMはパラグラフ直下でもリスト記法を扱える"""
        # Note: 普通のMarkdownはパラグラフ直下だとリストと認識されない
        original = (
            "foobar\n"
            "- first\n"
            "- second\n"
        )
        value = parse_kfm(original)
        self.assertIn("<ul>", value)
        self.assertIn("<li>", value)

    def test_parse_kfm_youtube_urls(self):
        """KFMはYouTube URL展開が行われる"""
        original = "foo https://www.youtube.com/watch?v=LoH0dOyyGx8 bar"
        value = parse_kfm(original)
        expected = (
            """<iframe width="640" height="360" """
            """src="//www.youtube.com/embed/LoH0dOyyGx8" """
            """frameborder="0" allowfullscreen></iframe>"""
        )
        self.assertIn(expected, value)

    def test_parse_kfm_nicovideo_urls(self):
        """KFMはYouTube URL展開が行われる"""
        original = "foo http://www.nicovideo.jp/watch/sm9 bar"
        value = parse_kfm(original)
        expected = (
            """<script type="text/javascript" """
            """src="http://ext.nicovideo.jp/thumb_watch/sm9">"""
            """</script>"""
        )
        self.assertIn(expected, value)

    def test_parse_kfm_mention(self):
        """KFMは@usernameを展開"""
        PersonaFactory(username='kawaztan_mention')
        original = "@kawaztan_mention\n@kawaztan_unknown"
        value = parse_kfm(original)
        expected = (
            """<span class="mention">"""
            """<a href="/members/kawaztan_mention/">"""
            """<img class="avatar avatar-small" src="/statics/img/defaults/persona_avatar_small.png">"""
            """<span class="mention-username">@kawaztan_mention</span></a>"""
            """</span>\n"""
            """@kawaztan_unknown"""
        )
        self.assertIn(expected, value)

    def test_parse_kfm_attachments(self):
        """KFMは添付ファイルシンタックスを展開"""
        material = MaterialFactory(content_file='kawaztan.png',
                                   author__username='kawaztan-material')
        slug = material.slug
        original = "{{attachments:{}}}\n".format(slug)
        value = parse_kfm(original)
        expected = (
            '<p><a href="/storage/attachments/kawaztan-material/kawaztan.png" '
            'rel="lightbox" data-lightbox="screenshots">\n    '
            '<img src="/storage/attachments/kawaztan-material/kawaztan.png" '
            'alt="kawaztan.png" style="max-width: 500px;" />\n'
            '</a></p>'
        )
        self.assertIn(expected, value)
