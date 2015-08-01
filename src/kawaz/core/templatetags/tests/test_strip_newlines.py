# coding=utf-8
"""
"""

from django.test import TestCase
from django.template import Template, Context


class StripNewlinesTemplateFilterTestCase(TestCase):

    def test_strip_newlines(self):
        """strip_newlinesフィルタで改行文字の除去が可能"""
        t = Template(
            """{% load strip_newlines %}"""
            """{{ body|strip_newlines }}"""
        )
        r = t.render(Context(dict(
            body="foo\rbar\nhoge\r\npiyo",
        )))
        self.assertIn('foobarhogepiyo', r)

    def test_strip_newlines(self):
        """strip_newlinesフィルタで改行文字の置換が可能"""
        t = Template(
            """{% load strip_newlines %}"""
            """{{ body|strip_newlines:'@' }}"""
        )
        r = t.render(Context(dict(
            body="foo\rbar\nhoge\r\npiyo\n\npiyo",
        )))
        self.assertIn('foo@bar@hoge@piyo@@piyo', r)
