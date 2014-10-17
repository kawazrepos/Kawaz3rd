# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.template import Context
from ..registry import registry


class ActivityNotifier(object):
    typename = None

    def get_typename(self):
        return self.typename

    def notify(self, activity, **kwargs):
        context = Context({
            'activity': activity,
            'object': activity.snapshot,
            'typename': self.get_typename(),
        })
        mediator = registry.get(activity)
        rendered = mediator.render(activity, context, self.get_typename())
        self.send(rendered, **kwargs)

    def send(self, rendered, **kwargs):
        raise NotImplementedError

