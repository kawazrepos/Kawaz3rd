from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.tests.utils import create_role_users
from .factories import EntryFactory, CategoryFactory


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

    def _render_template_with_author(self, username, author):
        t = Template(
            "{% load blogs_tags %}"
            "{% get_published_entries_of user as entries %}"
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r, user=author))
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

    def test_get_published_entries_of(self):
        """get_published_entriesは特定のユーザーが書いた公開状態の物のみを返す"""
        EntryFactory(pub_state='public', author=self.author)
        EntryFactory(pub_state='protected', author=self.author)
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
            entries = self._render_template_with_author(username, self.users['author'])
            self.assertEqual(entries.count(), nentries,
                             "{} should have {} entries.".format(username,
                                                                 nentries))

    def test_get_categories(self):
        """
        get_categoriesタグで全てのユーザーの持つカテゴリーが取り出せる
        """
        t = Template(
            "{% load blogs_tags %}"
            "{% get_categories as categories %}"
        )
        CategoryFactory()
        CategoryFactory()
        CategoryFactory()
        CategoryFactory()
        patterns = (
            ('adam', 4),
            ('seele', 4),
            ('nerv', 4),
            ('children', 4),
            ('wille', 4),
            ('anonymous', 4),
            ('author', 4),
        )
        r = MagicMock()
        for username, ncategories in patterns:
            c = Context(dict(request=r))
            r = t.render(c)
            # get_blog_entries は何も描画しない
            self.assertEqual(r.strip(), "")

            self.assertEqual(len(c['categories']), ncategories)

    def test_get_categories_with_user(self):
        """
        get_categoriesタグで特定のユーザーの持つカテゴリーが取り出せる
        """
        t = Template(
            "{% load blogs_tags %}"
            "{% get_categories user as categories %}"
        )
        CategoryFactory(author=self.users['children'])
        CategoryFactory(author=self.users['children'], label="日記")
        CategoryFactory(author=self.users['seele'])
        CategoryFactory()
        patterns = (
            ('adam', 0),
            ('seele', 1),
            ('nerv', 0),
            ('children', 2),
            ('wille', 0),
            ('anonymous', 0),
            ('author', 0),
        )
        r = MagicMock()
        for username, ncategories in patterns:
            c = Context(dict(request=r, user=self.users[username]))
            r = t.render(c)
            # get_blog_entries は何も描画しない
            self.assertEqual(r.strip(), "")

            self.assertEqual(len(c['categories']), ncategories)