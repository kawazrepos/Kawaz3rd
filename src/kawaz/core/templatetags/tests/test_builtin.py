#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/8
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context


class CustomBuiltInTemplateTagTestCase(TestCase):

    def test_markdown(self):
        """
        markdownがbuilt in template-filter化されている
        """
        t = Template(
            """{{ body | markdown }}"""
        )
        c = Context({
            'body' : "Hello"
        })
        self.assertIsNotNone(t.render(c))

