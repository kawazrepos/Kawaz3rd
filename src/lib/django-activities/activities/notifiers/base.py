# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.core.exceptions import ImproperlyConfigured
from ..registry import registry


class ActivityNotifierBase(object):
    include = None
    exclude = None

    def notify(self, text, **kwargs):
        raise NotImplementedError

    def connect(self, model):
        """
        Connect to the model. It is called in `Registry.register` method thus
        users should not call this method directly
        """
        if not registry.is_registered(model):
            raise ImproperlyConfigured(
                "{} model have not connected to any mediators."
            )
        self.model = model
        self.app_label = model._meta.app_label
        self.mediator = registry.get_for_model(model)
        self.mediator.add_notifier(self)


    def get_template_names(self, activity):
        """
        Get a list of template name used to render the activity
        """
        app_label = self.app_label
        model = self.model.__name__.lower()
        status = activity.status
        return (
            "activities/{}/{}_{}.txt".format(app_label, model, status),
            "activities/{}/{}.txt".format(app_label, status),
            "activities/{}.txt".format(status),
        )

    def prepare_context(self, activity, context):
        """
        Prepare context which used in 'render' method.
        """
        context.update({
            'activity': activity,
            'object': activity.snapshot
        })
        return context

    def render(self, activity, context):
        """
        Return rendered string of the specified activity
        """
        template_names = self.get_template_names(activity)
        template = select_template(template_names)
        context = self.prepare_context(activity, context.new())
        return template.render(context)
