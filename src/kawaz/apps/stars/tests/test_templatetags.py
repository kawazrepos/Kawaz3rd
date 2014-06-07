from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.utils import create_role_users
from .factories import StarFactory, ArticleFactory


class StarsTemplateTagTestCase(TestCase):
    def setUp(self):
        self.users = create_role_users()
        self.articles = dict(
            public=ArticleFactory(pub_state='public'),
            protected=ArticleFactory(pub_state='protected'),
            draft=ArticleFactory(pub_state='draft'),
        )
        self.stars = (
            StarFactory(content_object=self.articles['public']),
            StarFactory(content_object=self.articles['public']),
            StarFactory(content_object=self.articles['public']),
            StarFactory(content_object=self.articles['protected']),
            StarFactory(content_object=self.articles['protected']),
            StarFactory(content_object=self.articles['draft']),
        )

    def _render_stars_template(self, username, lookup=''):
        t = Template(
            "{{% load stars_tags %}}"
            "{{% get_stars {} as stars %}}".format(
                "'{}'".format(lookup) if lookup else ''
            )
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r))
        r = t.render(c)
        # get_stars は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['stars']

    def _render_endpoint_template(self, object):
        t = Template(
            "{{% load stars_tags %}}"
            "{{% get_star_endpoint {} as star_endpoint %}}".format(
                "object"
            )
        )
        r = MagicMock()
        c = Context(dict(request=r, object=object))
        r = t.render(c)
        # get_star_endpoint は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['star_endpoint']

    def test_get_stars_published(self):
        """get_stars published はユーザーが閲覧可能な Star を返す"""
        patterns = (
            ('adam', 5),
            ('seele', 5),
            ('nerv', 5),
            ('children', 5),
            ('wille', 3),
            ('anonymous', 3),
        )
        # with lookup
        for username, nstars in patterns:
            stars = self._render_stars_template(username, lookup='published')
            self.assertEqual(stars.count(), nstars,
                             "{} should see {} stars.".format(username,
                                                              nstars))
        # without lookup
        for username, nstars in patterns:
            stars = self._render_stars_template(username)
            self.assertEqual(stars.count(), nstars,
                             "{} should see {} stars.".format(username,
                                                              nstars))

    def test_get_stars_unknown(self):
        """get_stars unknown はエラーを出す"""
        patterns = (
            ('adam', 0),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
        )
        # with lookup
        for username, nstars in patterns:
            self.assertRaises(TemplateSyntaxError, self._render_stars_template,
                              username, lookup='unknown')

    def test_get_star_endpoint(self):
        """
        get_star_endpointはあるオブジェクトへのAPIエンドポイントを返す
        """
        from django.contrib.contenttypes.models import ContentType
        obj0 = ArticleFactory()
        obj1 = ArticleFactory()
        obj2 = ArticleFactory()
        ct = ContentType.objects.get_for_model(obj0)
        for obj in [obj0, obj1, obj2]:
            endpoint = self._render_endpoint_template(obj)
            self.assertEqual(endpoint,
                             "/api/stars?content_type={}&object_id={}".format(ct.pk, obj.pk))
