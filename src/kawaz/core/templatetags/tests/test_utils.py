#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/28
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock


class PathMatchesTemplateTagTestCase(TestCase):


    def test_when_regex_then(self):
        '''
        when =~ <pattern> then <string>タグがpatternとマッチしたとき、<string>を返す
        '''
        t = Template(
            """{% load utils %}"""
            """{% when path =~ pattern then 'active' %}"""
        )
        request = MagicMock()
        request.path = '/members/giginet/'
        c = Context({
            'request':  request,
            'pattern': '^/members/.+/$'
        })
        render = t.render(c)
        self.assertEqual(render, 'active')

    def test_when_regex_then_not_matched_pattern(self):
        '''
        when =~ <pattern> then <string>タグがpatternとマッチしないとき、空白文字を返す
        '''
        t = Template(
            """{% load utils %}"""
            """{% when path =~ pattern then 'active' %}"""
        )
        request = MagicMock()
        request.path = '/projects/giginet/'
        c = Context({
            'request':  request,
            'pattern': '^/members/.+/$'
        })
        render = t.render(c)
        self.assertEqual(render, '')

    def test_when_regex_then_invalid_argument(self):
        '''
        when path =~ <pattern> then <string>タグのシンタックスが間違ってたら、TemplateSyntaxErrorを返す
        '''
        t = ("""{% load utils %}"""
             """{% when =~ pattern then 'active' %}""")
        self.assertRaises(TemplateSyntaxError, Template, t)

