#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/21
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context
from django.template.loader import render_to_string
from kawaz.core.personas.tests.factories import PersonaFactory

class ParserTemplateTagTestCase(TestCase):

    def _test_href_tag(self, before, after):
        c = Context({
            'body' : before
        })
        t = Template(
            """{% load parser %}"""
            """{{ body | parser }}"""
        )
        r = t.render(c)
        self.assertEqual(r.strip(), after.strip())

    def test_url_expand_tag_in_quote(self):
        """
        Youtube、ニコニコ動画、URL、mentionなど
        いろいろ混ざった物を正しく展開します
        """
        PersonaFactory(username='kawaztan_mention')
        before = ("http://www.kawaz.org/\n"
        "http://nicovideo.jp/watch/sm9/\n"
        """<a href="http://www.nicovideo.jp/watch/sm9">ニコニコ動画</a>\n"""
        """<a href="https://www.youtube.com/watch?v=LoH0dOyyGx8">YouTube</a>\n"""
        "<b>HTMLも使えます</b>\n"
        "http://www.google.com/\n"
        "https://www.facebook.com/\n"
        "https://www.youtube.com/watch?v=LoH0dOyyGx8\n"
        "hoge@kawaztan_mention.com\n"
        "@kawaztan_mention\n"
        "@kawaztan_unknown\n")

        after = ("""<p><a href="http://www.kawaz.org/" rel="nofollow">http://www.kawaz.org/</a>\n"""
                 """<a href="http://nicovideo.jp/watch/sm9/" rel="nofollow">http://nicovideo.jp/watch/sm9/</a>\n"""
                 """<a href="http://www.nicovideo.jp/watch/sm9">ニコニコ動画</a>\n"""
                 """<a href="https://www.youtube.com/watch?v=LoH0dOyyGx8">YouTube</a>\n"""
                 "<b>HTMLも使えます</b>\n"
                 """<a href="http://www.google.com/" rel="nofollow">http://www.google.com/</a>\n"""
                 """<a href="https://www.facebook.com/" rel="nofollow">https://www.facebook.com/</a></p>\n"""
                 """\n"""
                 """<iframe width="640" height="480" src="//www.youtube.com/embed/LoH0dOyyGx8" frameborder="0" allowfullscreen></iframe>\n"""
                 """\n"""
                 """<p><a href="mailto:hoge<a href="/users/kawaztan_mention/"><img src="None">@kawaztan_mention</a>.com">hoge<a href="/users/kawaztan_mention/"><img src="None">@kawaztan_mention</a>.com</a>\n"""
                 """<a href="/users/kawaztan_mention/"><img src="None">@kawaztan_mention</a>\n"""
                 "@kawaztan_unknown</p>")
        self._test_href_tag(before, after)
