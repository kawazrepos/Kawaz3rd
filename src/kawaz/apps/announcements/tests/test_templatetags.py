from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.utils import create_role_users
from .factories import AnnouncementFactory


class AnnouncementsTemplateTagTestCase(TestCase):
    def setUp(self):
        self.announcements = dict(
            public=AnnouncementFactory(pub_state='public'),
            protected=AnnouncementFactory(pub_state='protected'),
            draft=AnnouncementFactory(pub_state='draft'),
        )
        self.users = create_role_users()

    def _render_template(self, username, lookup=''):
        t = Template(
            "{{% load announcements_tags %}}"
            "{{% get_announcements {} as announcements %}}".format(
                "'{}'".format(lookup) if lookup else ''
            )
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r))
        r = t.render(c)
        # get_announcements は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['announcements']

    def test_get_announcements_published(self):
        """get_announcements published はユーザーに対して公開された記事を返す"""
        patterns = (
            ('adam', 2),
            ('seele', 2),
            ('nerv', 2),
            ('children', 2),
            ('wille', 1),
            ('anonymous', 1),
        )
        # with lookup
        for username, nannouncements in patterns:
            announcements = self._render_template(username, lookup='published')
            self.assertEqual(announcements.count(), nannouncements)
        # without lookup
        for username, nannouncements in patterns:
            announcements = self._render_template(username)
            self.assertEqual(announcements.count(), nannouncements)

    def test_get_announcements_draft(self):
        """get_announcements draft はユーザーが編集可能な下書きを返す"""
        patterns = (
            ('adam', 1),
            ('seele', 1),
            ('nerv', 1),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
        )
        # with lookup
        for username, nannouncements in patterns:
            announcements = self._render_template(username, lookup='draft')
            self.assertEqual(announcements.count(), nannouncements)

    def test_get_announcements_unknown(self):
        """get_announcements unknown はエラーを出す"""
        patterns = (
            ('adam', 1),
            ('seele', 1),
            ('nerv', 1),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
        )
        # with lookup
        for username, nannouncements in patterns:
            self.assertRaises(TemplateSyntaxError, self._render_template,
                              username, lookup='unknown')
