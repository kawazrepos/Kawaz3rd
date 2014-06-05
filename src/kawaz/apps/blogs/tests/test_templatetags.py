from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.tests.utils import create_role_users
from .factories import EntryFactory


class BlogsTemplateTagTestCase(TestCase):
    def setUp(self):
        self.author = PersonaFactory(username='author', role='children')
        self.users = create_role_users({'author': self.author})
        self.entries = dict(
            public=EntryFactory(pub_state='public'),
            protected=EntryFactory(pub_state='protected'),
            draft=EntryFactory(pub_state='draft', author=self.author),
        )

    def _render_template(self, username, lookup=''):
        t = Template(
            "{{% load blogs_tags %}}"
            "{{% get_entries {} as entries %}}".format(
                "'{}'".format(lookup) if lookup else ''
            )
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r))
        r = t.render(c)
        # get_blog_entries は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['entries']

    def test_get_entries_published(self):
        """get_entries published はユーザーに対して公開された記事を返す"""
        patterns = (
            ('adam', 2),
            ('seele', 2),
            ('nerv', 2),
            ('children', 2),
            ('wille', 1),
            ('anonymous', 1),
            ('author', 2),
        )
        # with lookup
        for username, nentries in patterns:
            entries = self._render_template(username, lookup='published')
            self.assertEqual(entries.count(), nentries,
                             "{} should have {} entries.".format(username,
                                                                 nentries))
        # without lookup
        for username, nentries in patterns:
            entries = self._render_template(username)
            self.assertEqual(entries.count(), nentries,
                             "{} should have {} entries.".format(username,
                                                                 nentries))

    def test_get_entries_draft(self):
        """get_entries draft はユーザーが編集可能な下書きを返す"""
        patterns = (
            ('adam', 1),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
            ('author', 1),
        )
        # with lookup
        for username, nentries in patterns:
            entries = self._render_template(username, lookup='draft')
            self.assertEqual(entries.count(), nentries,
                             "{} should have {} entries.".format(username,
                                                                 nentries))

    def test_get_entries_unknown(self):
        """get_entries unknown はエラーを出す"""
        patterns = (
            ('adam', 0),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
            ('author', 0),
        )
        # with lookup
        for username, nentries in patterns:
            self.assertRaises(TemplateSyntaxError, self._render_template,
                              username, lookup='unknown')
