# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from ..conf import settings
from .base import ActivityNotifier


def get_notifiers(notifiers=None):
    """
    Get a class list of activity notifiers
    """
    if notifiers is None:
        notifiers = settings.ACTIVITIES_NOTIFIERS
    # list is not hashable thus convert it to tuple
    notifiers = tuple(notifiers)
    caches = getattr(get_notifiers, '_notifiers_caches')
    if notifiers not in caches:
        loaded_notifiers = []
        for i, notifier in enumerate(notifiers):
            if isinstance(notifier, str):
                module, cls = notifier.rsplit(".", 1)
                notifier = getattr(import_module(module), cls)
            if not issubclass(notifier, ActivityNotifier):
                raise ImproperlyConfigured((
                    "'{}' is not a subclass of ActivityNotifier"
                ).format(notifier))
            loaded_notifiers.append(notifier())
        caches[notifiers] = tuple(loaded_notifiers)
    return caches.get(notifiers)
get_notifiers._notifiers_caches = {}
