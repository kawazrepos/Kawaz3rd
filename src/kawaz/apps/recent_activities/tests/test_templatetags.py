#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/2
#

from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.utils import create_role_users
from ..models import RecentActivity
from .factories import RecentActivityFactory

__author__ = 'giginet'


class RecentActivityTemplateTagTestCase(TestCase):

    def _render_template(self):
        t = Template(
            "{% load recent_activities_tag %}"
            "{% get_recent_activities as recent_activities %}"
        )
        c = Context()
        r = t.render(c)
        # get_blog_products は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['recent_activities']

    def test_get_recent_activities(self):
        """
        get_recent_activitiesタグでrecent_activityの一覧を正常に取得できる
        """
        activities = [RecentActivityFactory() for i in range(3)]
        qs = self._render_template()
        self.assertEqual(len(qs), 3)
        self.assertEqual(qs[0], activities[0])
        self.assertEqual(qs[1], activities[1])
        self.assertEqual(qs[2], activities[2])
