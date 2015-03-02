# coding=utf-8
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType
from .mediator import ActivityMediator


class Registry(object):
    """
    An activity registry class
    """
    def __init__(self):
        self._registry = {}

    def _get_opts(self, model, for_concrete_model):
        if for_concrete_model:
            model = model._meta.concrete_model
        elif model._deferred:
            model = model._meta.proxy_for_model
        return model._meta

    def register(self, model, mediator=None, for_concrete_model=True):
        """
        Register a specified model to an ActivityMediator instance.

        Args:
            model (Model): A model of Django ORM
            mediator (instance): An ActivityMediator instance (or None).
                Default is None

        Raises:
            AttributeError: If the specified mediator is not an instance of
                ActivityMediator (or subclass of ActivityMediator).
        """
        if mediator is None:
            mediator = ActivityMediator()
        if not isinstance(mediator, ActivityMediator):
            raise AttributeError("'mediator' argument required to be an "
                                 "instance of ActivityMediator (sub)class.")
        # connect the model to the overseer
        mediator.connect(model)
        # register the mediator
        opts = self._get_opts(model, for_concrete_model)
        natural_key = "{}.{}".format(
            opts.app_label,
            opts.model_name,
        )
        self._registry[natural_key] = mediator

    def get(self, model_or_activity, for_concrete_model=True):
        """
        Get connected activity mediator of a model which the model connected
        or the activity has
        """
        from .models import Activity
        if isinstance(model_or_activity, Activity):
            model_or_activity = model_or_activity.content_type.model_class()
        elif isinstance(model_or_activity, Model):
            model_or_activity = model_or_activity.__class__
        opts = self._get_opts(model_or_activity, for_concrete_model)
        natural_key = "{}.{}".format(
            opts.app_label,
            opts.model_name,
        )
        return self._registry[natural_key]


# Create a global instance of registry
registry = Registry()
