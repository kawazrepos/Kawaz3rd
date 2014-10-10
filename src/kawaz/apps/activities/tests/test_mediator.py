# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from ..mediator import ActivityMediator
from ..models import Activity
from ..registry import Registry


class ActivitiesActivityMediatorTestCase(TestCase):
    @patch('kawaz.apps.activities.mediator.ContentType', spec=ContentType)
    @patch('kawaz.apps.activities.mediator.Activity', spec=Activity)
    def test__pre_delete_receiver(self, Activity, ContentType):
        ct = MagicMock()
        instance = MagicMock()
        instance.pk = 1
        activity = MagicMock()

        ContentType.objects.get_for_model.return_value = ct
        Activity.return_value = activity

        mediator = ActivityMediator()
        mediator.alter = MagicMock(return_value=activity)
        mediator._pre_delete_receiver(None, instance)

        Activity.assert_called_with(content_type=ct,
                                    object_id=instance.pk,
                                    status='deleted')
        # user defined alternation code is called
        mediator.alter.assert_called_with(instance, activity)
        # activity save method is called
        activity.save.assert_called_with()

    @patch('kawaz.apps.activities.mediator.ContentType', spec=ContentType)
    @patch('kawaz.apps.activities.mediator.Activity', spec=Activity)
    def test__post_save_receiver(self, Activity, ContentType):
        ct = MagicMock()
        instance = MagicMock()
        instance.pk = 1
        activity = MagicMock()

        ContentType.objects.get_for_model.return_value = ct
        Activity.return_value = activity

        mediator = ActivityMediator()
        mediator.alter = MagicMock(return_value=activity)
        mediator._post_save_receiver(None, instance, created=True)

        Activity.assert_called_with(content_type=ct,
                                    object_id=instance.pk,
                                    status='created')
        # user defined alternation code is called
        mediator.alter.assert_called_with(instance, activity)
        # activity save method is called
        activity.save.assert_called_with()

        mediator._post_save_receiver(None, instance, created=False)

        Activity.assert_called_with(content_type=ct,
                                    object_id=instance.pk,
                                    status='updated')
        # user defined alternation code is called
        mediator.alter.assert_called_with(instance, activity)
        # activity save method is called
        activity.save.assert_called_with()

    @patch('kawaz.apps.activities.mediator.ContentType', spec=ContentType)
    @patch('kawaz.apps.activities.mediator.Activity', spec=Activity)
    def test__m2m_changed_receiver(self, Activity, ContentType):
        ct = MagicMock()
        instance = MagicMock()
        instance.pk = 1
        activity = MagicMock()

        ContentType.objects.get_for_model.return_value = ct
        Activity.return_value = activity

        mediator = ActivityMediator()
        mediator.alter = MagicMock(return_value=activity)
        mediator._m2m_changed_receiver(None, instance, action='pre_add',
                                       reverse=False)

        # user defined alternation code is called
        mediator.alter.assert_called_with(instance, None,
                                          action='pre_add',
                                          reverse=False)
        # activity save method is called
        activity.save.assert_called_with()


    @patch('kawaz.apps.activities.mediator.post_save')
    @patch('kawaz.apps.activities.mediator.pre_delete')
    @patch('kawaz.apps.activities.mediator.m2m_changed')
    def test_connect(self, m2m_changed, pre_delete, post_save):
        model = MagicMock()
        model._meta.app_label = 'app_label'

        mediator = ActivityMediator()
        mediator.connect(model)
        self.assertEqual(mediator.model, model)
        self.assertEqual(mediator.app_label, 'app_label')

        post_save.connect.assert_called_with(mediator._post_save_receiver,
                                             sender=model,
                                             weak=False)
        pre_delete.connect.assert_called_with(mediator._pre_delete_receiver,
                                              sender=model,
                                              weak=False)
        m2m_changed.connect.assert_called_with(mediator._m2m_changed_receiver,
                                               sender=model,
                                               weak=False)

    def test_get_template_name(self):
        model = MagicMock()
        model.__name__ = MagicMock()
        model.__name__.lower = MagicMock(return_value='model')
        model._meta.app_label = 'app_label'
        activity = MagicMock()
        activity.status = 'status'

        mediator = ActivityMediator()
        mediator.connect(model)
        self.assertEqual(mediator.get_template_names(activity), (
                         'activities/app_label/model_status.html',
                         'activities/app_label/status.html',
                         'activities/status.html'))

    def test_prepare_context(self):
        activity = MagicMock()
        context = MagicMock()

        mediator = ActivityMediator()
        c = mediator.prepare_context(activity, context)

        context.update.assert_called_with({
            'activity': activity,
            'object': activity.content_object,
        })
        self.assertEqual(c, context)

    @patch('kawaz.apps.activities.mediator.select_template')
    def test_render(self, select_template):
        model = MagicMock()
        model.__name__ = MagicMock()
        model.__name__.lower = MagicMock(return_value='model')
        model._meta.app_label = 'app_label'
        activity = MagicMock()
        activity.status = 'status'
        context = MagicMock()
        rendered = MagicMock()
        template = MagicMock()
        template.render.return_value = rendered
        select_template.return_value = template

        mediator = ActivityMediator()
        mediator.connect(model)
        mediator.prepare_context = MagicMock(return_value=context.new())

        r = mediator.render(activity, context)

        select_template.assert_called_with(
            mediator.get_template_names(activity))
        mediator.prepare_context.assert_called_with(activity, context.new())
        template.render.assert_called_with(context.new())
        self.assertEqual(r, rendered)

