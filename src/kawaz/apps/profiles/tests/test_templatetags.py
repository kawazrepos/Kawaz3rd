from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.utils import create_role_users
from .factories import ProfileFactory


class ProfilesTemplateTagTestCase(TestCase):
    def setUp(self):
        self.users = create_role_users()
        self.profiles = (
            ProfileFactory(pub_state='public'),
            ProfileFactory(pub_state='public'),
            ProfileFactory(pub_state='public'),
            ProfileFactory(pub_state='protected'),
            ProfileFactory(pub_state='protected'),
        )
        # public/protected 共に最後のProfileのユーザーの is_active を False
        self.profiles[2].user.is_active = False
        self.profiles[2].user.save()
        self.profiles[4].user.is_active = False
        self.profiles[4].user.save()

    def _render_template(self, username, lookup=''):
        t = Template(
            "{{% load profiles_tags %}}"
            "{{% get_profiles {} as profiles %}}".format(
                "'{}'".format(lookup) if lookup else ''
            )
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r))
        r = t.render(c)
        # get_blog_profiles は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['profiles']

    def test_get_profiles_published(self):
        """get_profiles published はユーザーが閲覧可能なプロフィールを返す"""
        patterns = (
            ('adam', 3),
            ('seele', 3),
            ('nerv', 3),
            ('children', 3),
            ('wille', 2),
            ('anonymous', 2),
        )
        # with lookup
        for username, nprofiles in patterns:
            profiles = self._render_template(username, lookup='published')
            self.assertEqual(profiles.count(), nprofiles,
                             "{} should see {} profiles.".format(username,
                                                                 nprofiles))
        # without lookup
        for username, nprofiles in patterns:
            profiles = self._render_template(username)
            self.assertEqual(profiles.count(), nprofiles,
                             "{} should see {} profiles.".format(username,
                                                                 nprofiles))

    def test_get_profiles_unknown(self):
        """get_profiles unknown はエラーを出す"""
        patterns = (
            ('adam', 0),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
        )
        # with lookup
        for username, nprofiles in patterns:
            self.assertRaises(TemplateSyntaxError, self._render_template,
                              username, lookup='unknown')
