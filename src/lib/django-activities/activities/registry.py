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

    def register(self, model, mediator=None):
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
        self._registry[model] = mediator

    def get(self, model_or_activity):
        """
        Get connected activity mediator of a model which the model connected
        or the activity has
        """
        from .models import Activity
        if isinstance(model_or_activity, Activity):
            model_or_activity = model_or_activity.content_type.model_class()
        elif isinstance(model_or_activity, Model):
            model_or_activity = model_or_activity.__class__
        return self._registry[model_or_activity]


# Create a global instance of registry
registry = Registry()
