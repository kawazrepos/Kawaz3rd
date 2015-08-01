from django.test import TestCase, override_settings
from django.template import Template, Context


class SettingsTemplateTagTestCase(TestCase):

    @override_settings(key='value')
    def test_settings(self):
        """
        settingsタグでsettingsに指定した文字列を取得できる
        """
        t = Template(
            """{% load settings %}"""
            """{% settings 'key' %}"""
        )
        c = Context()
        render = t.render(c)
        self.assertEqual(render, 'value')

    def test_settings_with_undefined(self):
        """
        settingsタグでsettingsに指定した変数がないとき、空白文字が返る
        """
        t = Template(
            """{% load settings %}"""
            """{% settings 'key' %}"""
        )
        c = Context()
        render = t.render(c)
        self.assertEqual(render, '')

