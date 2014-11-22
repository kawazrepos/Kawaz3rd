# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.template import Context
from django.contrib.sites.models import Site


class ActivityNotifierBase(object):
    """
    A base class of activity notifier
    """
    typename = None

    def get_typename(self):
        """
        Get typename which is used to render the activity content.
        It simply return the value of 'typename' attribute in default.
        """
        return self.typename

    def render(self, activity, context, typename=None):
        """
        Return rendered string of the specified activity
        """
        from ..registry import registry as activity_registry
        mediator = activity_registry.get(activity)
        return mediator.render(activity, context, typename)

    def notify(self, activity, context=None, typename=None):
        """
        Notify the activity change via 'send' method of this instance
        """
        if typename is None:
            typename = self.get_typename()
        if context is None:
            context = Context({
                'site': Site.objects.get_current(),
            })
            # TODO Test me!!!
            # 実際にrenderのcontextとして`site`が渡されているかテストされていない
            # (notifierのテストではMediatorのMockを使っているため)
        rendered_content = self.render(activity, context, typename)
        # send rendered content via 'send' method
        self.send(rendered_content)

    def send(self, rendered_content):
        raise NotImplementedError(
            "Subclass of ActivityNotifierBase must override 'send' method"
        )
