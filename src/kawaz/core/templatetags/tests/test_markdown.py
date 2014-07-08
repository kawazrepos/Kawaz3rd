#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/8
#
__author__ = 'giginet'

from django.test import TestCase
from django.template import Template, Context


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
                 "<p>This is the text of the note.&nbsp;"
                 """<a href="#fnref-note-id" class="footnoteBackLink" title="Jump back to footnote 1 in the text.">&#8617;</a></p>\n"""
                 "</li>\n"
                 "</ol>\n"
                 "</div>\n")
        self._test_markdown(before, after)
