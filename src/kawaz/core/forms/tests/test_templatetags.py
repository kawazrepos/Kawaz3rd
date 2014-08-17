# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/17
#
__author__ = 'giginet'
from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from ..helpers import Bootstrap3HorizontalFormHelper


class GetFormHelperTemplateTagTestCase(TestCase):
    def _render_template(self, type=''):
        t = Template(
            "{{% load form_helper %}}"
            "{{% get_form_helper {} as helper %}}".format(
                "'{}'".format(type) if type else ''
            )
        )
        c = Context()
        r = t.render(c)
        # get_blog_helper は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['helper']

    def test_get_helper_horizontal(self):
        """get_helper horizontalでBootstrap3HorizontalFormHelperを取り出せる"""
        helper = self._render_template(type='horizontal')
        self.assertEqual(type(helper), Bootstrap3HorizontalFormHelper)

    def test_get_helper_unknown(self):
        """get_helperに存在しないtypeを渡したとき、TemplateSyntaxErrorが返る"""
        self.assertRaises(TemplateSyntaxError, self._render_template, 'unknown')
