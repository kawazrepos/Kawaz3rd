#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/9
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context
from django.template.loader import render_to_string
from kawaz.core.personas.tests.factories import PersonaFactory

class MentionTemplateTagTestCase(TestCase):

    def _test_mention_tag(self, before, after):
        c = Context({
            'body' : before
        })
        t = Template(
            """{% load mention %}"""
            """{{ body | mention }}"""
        )
        r = t.render(c)
        self.assertEqual(r.strip(), after.strip())

    def _expand_mention_tag(self, user):
        html = render_to_string("templatetags/mention.html", {
            'user' : user
        }).replace('\n', '')
        return html

    def test_with_exist_user(self):
        """
        存在するユーザーに対して言及したとき、展開される
        """
        kawaztan = PersonaFactory(username='kawaztan_mention0')
        tag = self._expand_mention_tag(kawaztan)
        before = """
        みんなのアイドルです @kawaztan_mention0
        """
        after = """
        みんなのアイドルです {}
        """.format(tag)

        self._test_mention_tag(before, after)

    def test_with_unknown_user(self):
        """
        存在しないユーザーに対して言及したとき、展開されない
        """
        before = """
        みんなのアイドルです @unknown_kawaztan
        """
        after = before

        self._test_mention_tag(before, after)

    def test_with_exist_user_multiple(self):
        """
        複数の存在するユーザーに対して言及したとき、展開される
        """
        kawaztan = PersonaFactory(username='kawaztan_mention1')
        geekdrums = PersonaFactory(username='geekdrums')
        tag = self._expand_mention_tag(kawaztan)
        tag2 = self._expand_mention_tag(geekdrums)
        before = """
        みんなのアイドルです @kawaztan_mention1
        神、いわゆるゴッドです @geekdrums
        """
        after = """
        みんなのアイドルです {}
        神、いわゆるゴッドです {}
        """.format(tag, tag2)

        self._test_mention_tag(before, after)

    def test_with_unknown_user_multiple(self):
        """
        複数の存在するユーザーと存在しないユーザーを混ぜて言及したとき、展開される
        """
        geekdrums = PersonaFactory(username='geekdrums')
        tag = self._expand_mention_tag(geekdrums)
        before = """
        みんなのアイドルです @unknown_kawaztan
        神、いわゆるゴッドです @geekdrums
        """
        after = """
        みんなのアイドルです @unknown_kawaztan
        神、いわゆるゴッドです {}
        """.format(tag)

        self._test_mention_tag(before, after)