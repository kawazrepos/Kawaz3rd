# ! -*- coding: utf-8 -*-
#
#
#


import os
from django.test import TestCase
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from .factories import MaterialFactory

class AttachmentTemplateTagTestCase(TestCase):

    def _test_attachments_tag(self, before, after):
        c = Context({
            'body' : before
        })
        t = Template(
            """{% load attachments %}"""
            """{{ body | parse_attachments }}"""
        )
        r = t.render(c)
        self.assertEqual(r.strip(), after.strip())

    def _expand_attachments_tag(self, material, kind):
        html = render_to_string(os.path.join("attachments", 'embed', '{}.html'.format(kind)), {
            'material' : material,
        })
        return mark_safe(html)

    def _test_with_filetype(self, filename, type):
        material = MaterialFactory(content_file=filename)
        before = """
        みんなのアイドルです {attachments:%s}
        """ % (material.slug)

        tag = self._expand_attachments_tag(material, type)

        after = """
        みんなのアイドルです {}
        """.format(tag)

        self._test_attachments_tag(before, after)

    def test_with_invalid_slug(self):
        before = """
        みんなのアイドルです {attachments:aaaaaaaaaaaaaaaaaa}
        """
        after = before
        self._test_attachments_tag(before, after)

    def test_with_image(self):
        """
        画像ファイルのサムネイルが展開される
        """
        self._test_with_filetype("kawaztan.jpg", "image")

    def test_with_audio(self):
        """
        音声ファイルのサムネイルが展開される
        """
        self._test_with_filetype("kawaztan.mp3", "audio")

    def test_with_movie(self):
        """
        動画のサムネイルが展開される
        """
        self._test_with_filetype("kawaztan.mov", "movie")

    def test_with_pdf(self):
        """
        PDFのサムネイルが展開される
        """
        self._test_with_filetype("kawaztan.pdf", "pdf")

    def test_with_etc(self):
        """
        その他のサムネイルが展開される
        """
        self._test_with_filetype("kawaztan.zip", "etc")
