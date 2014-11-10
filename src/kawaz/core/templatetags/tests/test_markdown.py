#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/8
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from ..templatetags.markdown import markdown


class RenderMarkdownTemplateTagTestCase(TestCase):

    def test_with_template(self):
        """
        render_markdownタグでテンプレートを展開して描画できるかを確かめます
        """
        t = Template(
            """{% load markdown %}"""
            """{% render_markdown 'testcases/markdown.md' %}"""
        )
        c = Context()
        render = t.render(c)
        after = mark_safe(markdown(render_to_string('testcases/markdown.md')))
        self.assertEqual(render, after)

class MarkdownTemplateTagTestCase(TestCase):

    def _test_markdown(self, body, after):
        t = Template(
            """{% load markdown %}"""
            """{{ body | markdown }}"""
        )
        c = Context({
            'body' : body
        })
        render = t.render(c)
        self.assertEqual(render, after)

    def test_with_markdown(self):
        '''
        普通のmarkdownが展開できる
        '''
        before = ("# 見出しです\n"
                  "## h2です\n"
                  "### h3です")

        after = ("<h1>見出しです</h1>\n\n"
                 "<h2>h2です</h2>\n\n"
                 "<h3>h3です</h3>\n")
        self._test_markdown(before, after)

    def test_markdown_with_code_friendly(self):
        '''
        extras = code-friendlyが効いている
        '''
        before = ("_hello_\n"
                  "__world__")
        after = ("<p>_hello_\n"
                  "__world__</p>\n")
        self._test_markdown(before, after)

    def test_markdown_with_html(self):
        '''
        markdown内にHTMLも記述できる

        Notice:
            全てのHTMLを許可している理由は
            markdownフィルタのdocstringを参照のこと
        '''
        before = ("# h1\n"
                  "<div>HTMLタグも効く</div>\n"
                  """<a href="http://www.google.co.jp/">リンクです</a>"""
        )
        after = ("<h1>h1</h1>\n\n"
                 "<div>HTMLタグも効く</div>\n\n"
                 """<p><a href="http://www.google.co.jp/">リンクです</a></p>\n"""
        )
        self._test_markdown(before, after)

    def test_markdown_with_footnote(self):
        '''
        extras = footnotesが効いている
        '''
        before = ("This is a paragraph with a footnote. [^note-id]\n"
                  "[^note-id]: This is the text of the note.")
        after = ("<p>This is a paragraph with a footnote. "
                 """<sup class="footnote-ref" id="fnref-note-id">"""
                 """<a href="#fn-note-id">1</a></sup></p>\n\n"""
                 """<div class="footnotes">\n"""
                 "<hr />\n"
                 "<ol>\n"
                 """<li id="fn-note-id">\n"""
                 "<p>This is the text of the note.&#160;"
                 """<a href="#fnref-note-id" class="footnoteBackLink" title="Jump back to footnote 1 in the text.">&#8617;</a></p>\n"""
                 "</li>\n"
                 "</ol>\n"
                 "</div>\n")
        self._test_markdown(before, after)

    def test_markdown_with_table(self):
        '''
        extras = tablesが効いている
        '''
        before = ('''| Header 1 | *Header* 2 |\n'''
                  '''| -------- | -------- |\n'''
                  '''| `Cell 1` | [Cell 2](http://example.com) link |\n'''
                  '''| Cell 3 | **Cell 4** |\n''')
        after = ('''<table>\n'''
                 '''<thead>\n'''
                 '''<tr>\n'''
                 '''  <th>Header 1</th>\n'''
                 '''  <th><em>Header</em> 2</th>\n'''
                 '''</tr>\n'''
                 '''</thead>\n'''
                 '''<tbody>\n'''
                 '''<tr>\n'''
                 '''  <td><code>Cell 1</code></td>\n'''
                 '''  <td><a href="http://example.com">Cell 2</a> link</td>\n'''
                 '''</tr>\n'''
                 '''<tr>\n'''
                 '''  <td>Cell 3</td>\n'''
                 '''  <td><strong>Cell 4</strong></td>\n'''
                 '''</tr>\n'''
                 '''</tbody>\n'''
                 '''</table>\n''')
        self._test_markdown(before, after)


class BlockMarkdownTemplateTagTestCase(TestCase):

    def test_block_markdown(self):
        """
        {% markdown %}
        {% endmarkdown %}
        に囲まれたMarkdownがHTMLにレンダリングされる
        """
        markdown_text = """かわずたん！ [こちら](http://www.kawaz.org/)"""
        t = Template(
            """{{% load markdown %}}"""
            """{{% markdown %}}"""
            """{}"""
            """{{% endmarkdown %}}""".format(markdown_text)
        )
        c = Context()
        render = t.render(c)
        after = mark_safe(markdown(markdown_text))
        self.assertEqual(render, after)