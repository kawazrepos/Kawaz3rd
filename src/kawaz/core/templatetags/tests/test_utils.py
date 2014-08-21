#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/28
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context
from unittest.mock import MagicMock


class ActiveTemplateTagTestCase(TestCase):

    def test_active(self):
        '''
        activeタグのpatternが現在のURLとマッチしたとき、activeの文字を返す
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

    def test_active_contains_get_parametter(self):
        """
        activeタグはGETパラメータの値も含む
        """
        t = Template(
            """{% load utils %}"""
            """{% active pattern %}"""
        )
        request = MagicMock()
        request.path = '/members/?o=username$'
        c = Context({
            'request':  request,
            'pattern': '.+?o=username'
        })
        render = t.render(c)
        self.assertEqual(render, 'active')

    def test_active_with_not_matched_pattern(self):
        '''
        activeタグのpatternが現在のURLとマッチしないとき、空白文字を返す
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
