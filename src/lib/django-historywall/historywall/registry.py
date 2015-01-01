# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from .mediator import Mediator


class Registry(object):
    """
    An activity registry class
    """
    def __init__(self):
        self._registry = {}

    def register(self, model, mediator=None):
        """
        Register a specified model to a Mediator instance.

        Args:
            model (Model): A model of Django ORM
            mediator (instance): A Mediator instance (or None).
                Default is None

        Raises:
            AttributeError: If the specified mediator is not an instance of
                Mediator (or subclass of Mediator).
        """
        if mediator is None:
            mediator = Mediator()
        if not isinstance(mediator, Mediator):
            raise AttributeError("'mediator' argument required to be an "
                                 "instance of Mediator (sub)class.")
        # connect the model to the overseer
        mediator.connect(model)
        self._registry[model] = mediator

    def get(self, wall):
        """
        Get connected mediator of a model which the wall refer.
        """
        model = wall.content_type.model_class()
        return self._registry[model]


# Create a global instance of registry
registry = Registry()
