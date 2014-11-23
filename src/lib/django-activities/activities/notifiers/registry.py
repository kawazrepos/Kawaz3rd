# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from .base import ActivityNotifierBase


class Registry(object):
    """
    An activity notifier registry class
    """
    def __init__(self):
        self._registry = {}

    def _prefer_repr(self, str_or_cls):
        if not isinstance(str_or_cls, str):
            if isinstance(str_or_cls, ActivityNotifierBase):
                return repr(str_or_cls.__class__)
            else:
                return repr(str_or_cls)
        return str_or_cls

    def register(self, notifier, name=None, overwrite=True):
        """
        Register a notifier instance as specified name
        """
        if not isinstance(notifier, ActivityNotifierBase):
            raise AttributeError(
                "'notifier' argument requred to be an instance "
                "of ActivityNotifierBase (sub)class."
            )
        name = self._prefer_repr(name or notifier)
        if not overwrite and name in self:
            raise AttributeError((
                "'{}' is already registered. "
                "Use different name to register."
            ).format(name))
        self._registry[name] = notifier
        return notifier

    def get_or_register(self, notifier, name=None):
        name = self._prefer_repr(name or notifier)
        if name not in self:
            self.register(notifier, name)
        return self.get(name)

    def __contains__(self, name_or_cls):
        name = self._prefer_repr(name_or_cls)
        return name in self._registry

    def get(self, name_or_cls):
        name = self._prefer_repr(name_or_cls)
        return self._registry[name]


# Create a global instance of registry
registry = Registry()
