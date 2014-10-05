# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.template import Template, Context
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import SafeBytes
from .models import ActivitiesTestModelA as ModelA
from .models import ActivitiesTestModelB as ModelB
from .models import ActivitiesTestModelC as ModelC
from ..models import Activity
from ..registry import registry


class ActivitiesTemplateTagsActivitiesTagsTestCase(TestCase):
    def setUp(self):
        self.models = (
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelA.objects.create(text='a'),
            ModelB.objects.create(text='b'),
            ModelB.objects.create(text='b'),
            ModelC.objects.create(text='c'),
        )
        self.activities = []
        for i, model in enumerate(self.models):
            ct = ContentType.objects.get_for_model(model)
            pk = model.pk
            self.activities.extend([
                Activity.objects.create(content_type=ct,
                                        object_id=pk,
                                        status='created'),
                Activity.objects.create(content_type=ct,
                                        object_id=pk,
                                        status='updated'),
                Activity.objects.create(content_type=ct,
                                        object_id=pk,
                                        status='deleted'),
            ])

    def test_get_activities(self):
        t = Template(
            "{% load activities_tags %}"
            "{% get_activities as activities %}"
        )
        c = Context()
        r = t.render(c)
        # get_activities should not render anything
        self.assertEqual(r.strip(), '')
        # activities should be equal to activity queryset
        # but the queryset is difer thus cannot compare directly
        self.assertEqual([x.pk for x in c['activities']],
                         [x.pk for x in Activity.objects.all()])

    def test_get_latest_activities(self):
        t = Template(
            "{% load activities_tags %}"
            "{% get_latest_activities as activities %}"
        )
        c = Context()
        r = t.render(c)
        # get_activities should not render anything
        self.assertEqual(r.strip(), '')
        # activities should be equal to activity queryset
        # but the queryset is difer thus cannot compare directly
        self.assertEqual([x.pk for x in c['activities']],
                         [x.pk for x in Activity.objects.latests()])

    @patch('kawaz.apps.activities.templatetags.activities_tags.registry')
    def test_render_activity(self, registry):
        activity = self.activities[0]
        mediator = MagicMock()
        mediator.render.return_value = '<strong>Hello</strong>'
        registry.get.return_value = mediator
        t = Template(
            "{% load activities_tags %}"
            "{% render_activity activity %}"
        )
        c = Context({'activity': activity})
        r = t.render(c)

        registry.get.assert_called_with(activity)
        mediator.render.assert_called_with(activity, c)
        self.assertEqual(r.strip(), '<strong>Hello</strong>')


