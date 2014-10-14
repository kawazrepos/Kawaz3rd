# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
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

    def get(self, activity):
        """
        Get connected activity mediator of a model which the activity has.
        """
        model = activity.content_type.model_class()
        return self._registry[model]


# Create a global instance of registry
registry = Registry()
