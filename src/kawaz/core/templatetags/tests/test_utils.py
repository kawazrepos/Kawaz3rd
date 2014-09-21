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

    def test_active_contains_get_parameter(self):
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


class GetWeekDayTemplateTagTestCase(TestCase):

    def test_weekday(self):
        '''
        get_week_dayで平日だったときにweekdayを返す
        '''
        import datetime
        t = Template(
            """{% load utils %}"""
            """{% get_week_day datetime %}"""
        )
        request = MagicMock()
        c = Context({
            'request':  request,
            'datetime': datetime.datetime(2014, 9, 22)
        })
        render = t.render(c)
        self.assertEqual(render, 'weekday')


    def test_saturday(self):
        '''
        get_week_dayで土曜だったときにsaturdayを返す
        '''
        import datetime
        t = Template(
            """{% load utils %}"""
            """{% get_week_day datetime %}"""
        )
        request = MagicMock()
        c = Context({
            'request':  request,
            'datetime': datetime.datetime(2014, 9, 20)
        })
        render = t.render(c)
        self.assertEqual(render, 'saturday')


    def test_sunday(self):
        '''
        get_week_dayで平日だったときにweekdayを返す
        '''
        import datetime
        t = Template(
            """{% load utils %}"""
            """{% get_week_day datetime %}"""
        )
        request = MagicMock()
        c = Context({
            'request':  request,
            'datetime': datetime.datetime(2014, 9, 21)
        })
        render = t.render(c)
        self.assertEqual(render, 'sunday')
