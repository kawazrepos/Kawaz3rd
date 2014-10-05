from django.test import TestCase
from django.template import Template, Context
from django.template.loader import render_to_string
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.apps.profiles.tests.factories import ProfileFactory
from kawaz.apps.attachments.tests.factories import MaterialFactory


class ParserTemplateTagTestCase(TestCase):

    def _test_parser_filter(self, content, expected, neg=False):
        c = Context({'content': content})
        t = Template(
            "{% load parser %}"
            "{{ content|parser }}"
        )
        r = t.render(c)
        if neg:
            self.assertFalse(expected in r,
                             "\n{} does contain \n{}".format(r, expected))
        else:
            self.assertTrue(expected in r,
                            "\n{} does not contain \n{}".format(r, expected))

    def test_parser_filter_expand_youtube_url(self):
        """
        parserフィルタはYouTubeのURLを展開
        """
        # URLのみの行がある場合は展開
        url = "https://www.youtube.com/watch?v=LoH0dOyyGx8"
        content = "foo\n{}\nbar".format(url)
        expected = (
            """<iframe width="640" height="360" """
            """src="//www.youtube.com/embed/LoH0dOyyGx8" """
            """frameborder="0" allowfullscreen></iframe>"""
        )
        self._test_parser_filter(content, expected)
        # URLのみの行が無い場合は展開しない
        content = "foo {} bar".format(url)
        self._test_parser_filter(content, expected, neg=True)

    def test_parser_filter_expand_nicovideo_url(self):
        """
        parserフィルタはニコニコ動画のURLを展開
        """
        # URLのみの行がある場合は展開
        url = "http://www.nicovideo.jp/watch/sm9"
        content = "foo\n{}\nbar".format(url)
        expected = (
            """<script type="text/javascript" """
            """src="http://ext.nicovideo.jp/thumb_watch/sm9">"""
            """</script>"""
        )
        self._test_parser_filter(content, expected)
        # URLのみの行が無い場合は展開しない
        content = "foo {} bar".format(url)
        self._test_parser_filter(content, expected, neg=True)

    def test_parser_filter_expand_url_and_mail_address(self):
        """
        parserフィルタはURLやメールアドレスをリンクとして展開
        """
        # URLのみの行がある場合は展開
        url = "http://www.kawaz.org/"
        mail = "foobar@kawaz.org"
        content = "foo\n{}\n{}\nbar".format(url, mail)
        expected = (
            """<a href="http://www.kawaz.org/" rel="nofollow">"""
            """http://www.kawaz.org/</a>\n"""
            """<a href="mailto:foobar@kawaz.org">foobar@kawaz.org</a>"""
        )
        self._test_parser_filter(content, expected)

    def test_parser_filter_expand_mention(self):
        """
        parserフィルタは@<username>を展開
        """
        user = PersonaFactory(username='kawaztan_mention')
        ProfileFactory(user=user)
        content = "@kawaztan_mention\n@kawaztan_unknown"
        expected = (
            """<a href="/members/kawaztan_mention/">"""
            """<img src="/statics/img/defaults/profile_small.png">@kawaztan_mention</a>\n"""
            """@kawaztan_unknown"""
        )
        self._test_parser_filter(content, expected)

    def test_parser_filter_expand_markdown(self):
        """
        parserフィルタはMarkdownをHTMlに展開
        """
        content = "**Markdown**\n<b>HTML</b>"
        expected = (
            """<strong>Markdown</strong>\n"""
            """<b>HTML</b>"""
        )
        self._test_parser_filter(content, expected)

    def test_parser_filter_expand_attachments(self):
        """
        parserフィルタは添付ファイルを展開
        """
        material = MaterialFactory(content_file='kawaztan.png',
                                   author__username='kawaztan-material')
        slug = material.slug
        content = "{{attachments:{}}}\n".format(slug)
        expected = (
            '<p><a href="/storage/attachments/kawaztan-material/kawaztan.png" '
            'rel="lightbox" data-lightbox="thumbnail">\n    '
            '<img src="/storage/attachments/kawaztan-material/kawaztan.png" '
            'alt="kawaztan.png" style="max-width: 600px;" />\n'
            '</a>\n</p>'
        )
        self._test_parser_filter(content, expected)
