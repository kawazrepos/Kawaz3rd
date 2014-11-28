from django.test import TestCase
from django.template.loader import render_to_string
from ...extras.autolink import parse_autolinks


class ParseAutoLinksTestCase(TestCase):

    def _render_template(self, url):
        return render_to_string('kfm/extras/autolink.html', {
            'url': url,
        }).strip()

    def test_parse_autolinks(self):
        """URLは展開される"""
        template_str = "http://www.kawaz.org/"
        value = parse_autolinks(template_str)
        self.assertEqual(value, self._render_template(template_str))

    def test_parse_autolinks_single_quoated(self):
        """シングルクォートされたURLは展開されない"""
        template_str = "'http://www.kawaz.org/'"
        original = template_str
        value = parse_autolinks(original)
        self.assertEqual(value, original)

    def test_parse_autolinks_double_quoated(self):
        """ダブルクォートされたURLは展開されない"""
        template_str = "\"http://www.kawaz.org/\""
        original = template_str
        value = parse_autolinks(original)
        self.assertEqual(value, original)

    def test_parse_autolinks_fenced(self):
        """フェンス化されたURLは展開されない"""
        template_str = "`http://www.kawaz.org/`"
        original = template_str
        value = parse_autolinks(original)
        self.assertEqual(value, original)

        template_str = "```\nhttp://www.kawaz.org/\n```"
        original = template_str
        value = parse_autolinks(original)
        self.assertEqual(value, original)

    def test_parse_autolinks_multiple(self):
        """複数のURLも正しく展開される"""
        template_str = (
            "全てはここから始まった\n"
            "http://www.kawaz.org/\n"
            "全く新しい体験\n"
            "http://www.kawaz.org/\n"
            "オススメ http://www.kawaz.org/\n"
            "http://www.kawaz.org/ かなり\n"
        )
        value = template_str
        value = parse_autolinks(value)
        self.assertEqual(value, (
            "全てはここから始まった\n"
            "{}\n"
            "全く新しい体験\n"
            "{}\n"
            "オススメ {}\n"
            "{} かなり\n"
        ).format(
            self._render_template("http://www.kawaz.org/"),
            self._render_template("http://www.kawaz.org/"),
            self._render_template("http://www.kawaz.org/"),
            self._render_template("http://www.kawaz.org/"),
        ))


