from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.tests.utils import create_role_users
from .factories import ProjectFactory


class ProjectsTemplateTagTestCase(TestCase):
    def setUp(self):
        self.administrator = PersonaFactory(username='administrator',
                                            role='children')
        self.users = create_role_users({'administrator': self.administrator})
        self.projects = (
            ProjectFactory(pub_state='public'),
            ProjectFactory(pub_state='public'),
            ProjectFactory(pub_state='public', status='eternal'),
            ProjectFactory(pub_state='protected'),
            ProjectFactory(pub_state='protected', status='eternal'),
            ProjectFactory(pub_state='draft',
                           administrator=self.administrator),
        )

    def _render_template(self, username, lookup=''):
        t = Template(
            "{{% load projects_tags %}}"
            "{{% get_projects {} as projects %}}".format(
                "'{}'".format(lookup) if lookup else ''
            )
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r))
        r = t.render(c)
        # get_blog_projects は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['projects']

    def test_get_projects_published(self):
        """get_projects published はユーザーが閲覧可能な Project を返す"""
        patterns = (
            ('adam', 5),
            ('seele', 5),
            ('nerv', 5),
            ('children', 5),
            ('wille', 3),
            ('anonymous', 3),
            ('administrator', 5),
        )
        # with lookup
        for username, nprojects in patterns:
            projects = self._render_template(username, lookup='published')
            self.assertEqual(projects.count(), nprojects,
                             "{} should see {} projects.".format(username,
                                                                 nprojects))
        # without lookup
        for username, nprojects in patterns:
            projects = self._render_template(username)
            self.assertEqual(projects.count(), nprojects,
                             "{} should see {} projects.".format(username,
                                                                 nprojects))

    def test_get_projects_draft(self):
        """get_projects draft はユーザーが編集可能な下書き Project を返す"""
        patterns = (
            ('adam', 1),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
            ('administrator', 1),
        )
        # with lookup
        for username, nprojects in patterns:
            projects = self._render_template(username, lookup='draft')
            self.assertEqual(projects.count(), nprojects,
                             "{} should see {} projects.".format(username,
                                                                 nprojects))

    def test_get_projects_active(self):
        """get_projects active はユーザーが閲覧可能なアクティブ Project を返す
        """
        patterns = (
            ('adam', 3),
            ('seele', 3),
            ('nerv', 3),
            ('children', 3),
            ('wille', 2),
            ('anonymous', 2),
            ('administrator', 3),
        )
        # with lookup
        for username, nprojects in patterns:
            projects = self._render_template(username, lookup='active')
            self.assertEqual(projects.count(), nprojects,
                             "{} should see {} projects.".format(username,
                                                                 nprojects))

    def test_get_projects_unknown(self):
        """get_projects unknown はエラーを出す"""
        patterns = (
            ('adam', 0),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
            ('administrator', 0),
        )
        # with lookup
        for username, nprojects in patterns:
            self.assertRaises(TemplateSyntaxError, self._render_template,
                              username, lookup='unknown')
