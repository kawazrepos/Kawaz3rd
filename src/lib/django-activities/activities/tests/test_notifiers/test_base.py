# coding=utf-8
"""
"""

from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.test.utils import override_settings
from ...notifiers.base import ActivityNotifierBase


class ActivityNotifierBaseTestCase(TestCase):
    def test_attributes(self):
        notifier = ActivityNotifierBase()
        self.assertTrue(hasattr(notifier, 'typename'))
        self.assertTrue(hasattr(notifier, 'get_typename'))
        self.assertTrue(hasattr(notifier, 'render'))
        self.assertTrue(hasattr(notifier, 'notify'))
        self.assertTrue(hasattr(notifier, 'send'))
        self.assertTrue(callable(getattr(notifier, 'get_typename')))
        self.assertTrue(callable(getattr(notifier, 'render')))
        self.assertTrue(callable(getattr(notifier, 'notify')))
        self.assertTrue(callable(getattr(notifier, 'send')))

    def test_get_typename(self):
        typename = MagicMock()
        notifier = ActivityNotifierBase()
        notifier.typename = typename
        self.assertEqual(notifier.get_typename(), typename)

    @patch('activities.registry.registry')
    def test_render(self, registry):
        rendered_content = MagicMock()
        mediator = MagicMock()
        mediator.render = MagicMock(return_value=rendered_content)
        registry.get = MagicMock(return_value=mediator)

        activity = MagicMock()
        context = MagicMock()
        typename = MagicMock()

        notifier = ActivityNotifierBase()
        notifier.render(activity, context, typename)

        registry.get.assert_called_with(activity)
        mediator.render.assert_called_with(activity,
                                           context,
                                           typename)

    def test_notify(self):
        typename = MagicMock()
        rendered_content = MagicMock()
        notifier = ActivityNotifierBase()
        notifier.get_typename = MagicMock(return_value=typename)
        notifier.render = MagicMock(return_value=rendered_content)
        notifier.send = MagicMock()

        activity = MagicMock()
        context = MagicMock()

        notifier.notify(activity, context, typename)
        notifier.get_typename.assert_not_called()
        notifier.render.assert_called_with(activity,
                                           context,
                                           typename)
        notifier.send.assert_called_with(rendered_content)

        notifier.notify(activity, context)
        notifier.get_typename.assert_not_called()
        notifier.render.assert_called_with(activity,
                                           context,
                                           typename)
        notifier.send.assert_called_with(rendered_content)

    def test_send(self):
        rendered_content = MagicMock()
        notifier = ActivityNotifierBase()
        self.assertRaises(NotImplementedError,
                          notifier.send,
                          rendered_content)
