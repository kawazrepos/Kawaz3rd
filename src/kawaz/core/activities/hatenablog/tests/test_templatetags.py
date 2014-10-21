from django.test import TestCase
from django.template import Template, Context
from .factories import HatenablogEntryFactory


class ActivitiesHatenablogEntryTemplateTagTestCase(TestCase):

    def _render_template(self):
        t = Template(
            "{% load activities_hatenablog_tag %}"
            "{% get_hatenablog_entries as entries %}"
        )
        c = Context()
        r = t.render(c)
        # このタグは何も描画しない
        self.assertEqual(r.strip(), "")
        return c['entries']

    def test_get_hatenablog_entries(self):
        """
        get_hatenablog_entries タグではてなブログの一覧を正常に取得できる
        """
        entries = [HatenablogEntryFactory() for i in range(3)]
        qs = self._render_template()
        self.assertEqual(len(qs), 3)
        self.assertEqual(qs[0], entries[0])
        self.assertEqual(qs[1], entries[1])
        self.assertEqual(qs[2], entries[2])
