# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from .mediator import ActivityMediator


class Registry(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, mediator=None):
        if mediator is None:
            mediator = ActivityMediator()
        if not isinstance(mediator, ActivityMediator):
            raise AttributeError("'mediator' argument required to be an "
                                 "instance of ActivityMediator (sub)class.")
        # connect the model to the overseer
        mediator.connect(model)
        self._registry[model] = mediator

    def get(self, activity):
        model = activity.content_object._meta.model
        return self._registry[model]


# Create a global instance of registry
registry = Registry()
