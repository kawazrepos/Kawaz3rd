# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.template.loader import render_to_string
from kawaz.core.personas.tests.factories import PersonaFactory
from ...extras.mention import parse_mentions


class ParseMentionsTestCase(TestCase):
    def setUp(self):
        self.users = (
            PersonaFactory(),
            PersonaFactory(),
            PersonaFactory(),
        )

    def _render_template(self, user):
        return render_to_string('kfm/extras/mention.html', {
            'user': user,
        }).strip()

    def test_parse_mentions_for_presence(self):
        """存在するユーザーに対してのメンションは展開される"""
        template_str = "@{}"
        for user in self.users:
            value = template_str.format(user.username)
            value = parse_mentions(value)
            self.assertEqual(value, self._render_template(user))

    def test_parse_mentions_for_absence(self):
        """存在しないユーザーに対してのメンションは無視される"""
        template_str = "@{}"
        for username in ('invalid_user', 'invalid_user2', 'hogehoge'):
            value = template_str.format(username)
            value = parse_mentions(value)
            self.assertEqual(value, template_str.format(username))

    def test_parse_mentions_for_single_quoted(self):
        """シングルクォートされたメンションは展開されない"""
        template_str = "'@{}'"
        for user in self.users:
            value = template_str.format(user.username)
            value = parse_mentions(value)
            self.assertEqual(value, template_str.format(user.username))

    def test_parse_mentions_for_double_quoted(self):
        """ダブルクォートされたメンションは展開されない"""
        template_str = "\"@{}\""
        for user in self.users:
            value = template_str.format(user.username)
            value = parse_mentions(value)
            self.assertEqual(value, template_str.format(user.username))

    def test_parse_mentions_for_fenced(self):
        """フェンス化されたメンションは展開されない"""
        template_str = "`@{}`"
        for user in self.users:
            value = template_str.format(user.username)
            value = parse_mentions(value)
            self.assertEqual(value, template_str.format(user.username))
        template_str = "```\n@{}\n```"
        for user in self.users:
            value = template_str.format(user.username)
            value = parse_mentions(value)
            self.assertEqual(value, template_str.format(user.username))

    def test_parse_mentions_for_bracket(self):
        """ブランケットで囲まれたメンションは展開されない"""
        template_str = "[@{}]"
        for user in self.users:
            value = template_str.format(user.username)
            value = parse_mentions(value)
            self.assertEqual(value, template_str.format(user.username))
        template_str = "(@{})"
        for user in self.users:
            value = template_str.format(user.username)
            value = parse_mentions(value)
            self.assertEqual(value, template_str.format(user.username))

    def test_parse_mentions_multiple(self):
        """複数のメンションが適切に展開される"""
        template_str = (
            "@{}\n"
            "@{}\n"
            "@{}\n"
            "@{}\n"
        )
        value = template_str.format(
            self.users[0].username,
            self.users[1].username,
            self.users[2].username,
            "invalid_username",
        )
        value = parse_mentions(value)
        self.assertEqual(value, "{}\n{}\n{}\n@{}\n".format(
            self._render_template(self.users[0]),
            self._render_template(self.users[1]),
            self._render_template(self.users[2]),
            "invalid_username",
        ))
