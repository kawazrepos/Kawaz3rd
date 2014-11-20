from django.test import TestCase
from django.template import Template, Context


class ExprTemplateTagTestCase(TestCase):

    def test_expr_render(self):
        """
        expr タグを利用して計算結果を描画可能
        """
        t = Template(
            """{% load expr %}"""
            """{% expr 1 + 1 %}"""
        )
        c = Context()
        render = t.render(c)
        self.assertTrue('2' in render)

        t = Template(
            """{% load expr %}"""
            """{% expr 1 + var1 %}"""
        )
        c = Context({'var1': 10})
        render = t.render(c)
        self.assertTrue('11' in render)

    def test_expr_render(self):
        """
        expr タグを利用して計算結果を代入可能
        """
        t = Template(
            """{% load expr %}"""
            """{% expr 1 + 1 as result %}"""
        )
        c = Context()
        render = t.render(c)
        self.assertFalse('2' in render)
        self.assertTrue('result' in c)
        self.assertEqual(c['result'], 2)

        t = Template(
            """{% load expr %}"""
            """{% expr 1 + var1 as result %}"""
        )
        c = Context({'var1': 10})
        render = t.render(c)
        self.assertFalse('11' in render)
        self.assertTrue('result' in c)
        self.assertEqual(c['result'], 11)

