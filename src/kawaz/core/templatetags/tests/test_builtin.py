#! -*- coding: utf-8 -*-
#
#
#


from django.test import TestCase
from django.template import Template, Context


class CustomBuiltInTemplateTagTestCase(TestCase):

    def test_kfm(self):
        """
        kfmがbuilt in template-filter化されている
        """
        t = Template(
            """{{ body | kfm }}"""
        )
        c = Context({
            'body' : "Hello"
        })
        self.assertIsNotNone(t.render(c))

