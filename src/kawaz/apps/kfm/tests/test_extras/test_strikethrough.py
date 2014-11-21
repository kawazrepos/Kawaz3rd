# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from unittest.mock import patch, MagicMock
from django.test import TestCase
from ...extras.strikethrough import parse_strikethroughs


class ParseStrikethroughsTestCase(TestCase):

    def test_parse_strikethroughs(self):
        """打ち消し構文が正しく変換される"""
        original = "~~Strike~~"
        value = parse_strikethroughs(original)
        self.assertEqual(value, "<del>Strike</del>")

    def test_parse_strikethroughs_single_quoted(self):
        """シングルクォートされた打ち消し構文は変換されない"""
        original = "'~~Strike~~'"
        value = parse_strikethroughs(original)
        self.assertEqual(value, original)

    def test_parse_strikethroughs_double_quoted(self):
        """ダブルクォートされた打ち消し構文は変換されない"""
        original = "\"~~Strike~~\""
        value = parse_strikethroughs(original)
        self.assertEqual(value, original)

    def test_parse_strikethroughs_fenced(self):
        """フェンス化された打ち消し構文は変換されない"""
        original = "`~~Strike~~`"
        value = parse_strikethroughs(original)
        self.assertEqual(value, original)

        original = "```\n~~Strike~~\n```"
        value = parse_strikethroughs(original)
        self.assertEqual(value, original)

    def test_parse_strikethroughs_multiple(self):
        """複数の打ち消し構文が正しく変換される"""
        original = (
            "~~Strike~~\n"
            "~=Not strike=~\n"
            "~~Through~~\n"
            "`~~Fenced~~`\n"
        )
        value = parse_strikethroughs(original)
        self.assertEqual(value, (
            "<del>Strike</del>\n"
            "~=Not strike=~\n"
            "<del>Through</del>\n"
            "`~~Fenced~~`\n"
        ))

