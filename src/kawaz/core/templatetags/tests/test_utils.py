#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/28
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context
from unittest.mock import MagicMock


class PathMatchesTemplateTagTestCase(TestCase):

    def test_string_by_path(self):
        '''
        string_by_pathタグがregexとマッチしたとき、第3引数の文字を返す
        '''
        t = Template(
            """{% load utils %}"""
            """{% active pattern %}"""
        )
        request = MagicMock()
        request.path = '/members/giginet/'
        c = Context({
            'request':  request,
            'pattern': '^/members/.+/$'
        })
        render = t.render(c)
        self.assertEqual(render, 'active')

    def test_string_by_path_with_not_matched_pattern(self):
        '''
        string_by_pathタグがregexとマッチしないとき、空白文字を返す
        '''
        t = Template(
            """{% load utils %}"""
            """{% active pattern %}"""
        )
        request = MagicMock()
        request.path = '/projects/giginet/'
        c = Context({
            'request':  request,
            'pattern': '^/members/.+/$'
        })
        render = t.render(c)
        self.assertEqual(render, '')
