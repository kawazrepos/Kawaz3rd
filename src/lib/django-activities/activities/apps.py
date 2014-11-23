# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import lru_cache
from importlib import import_module
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from .conf import settings
from .notifiers.registry import registry as notifier_registry


@lru_cache()
def get_class(path):
    """
    Return a class of a given the dotted Python import path (as a string).

    If the addition cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    """
    module, attr = path.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(
            'Error loading a module %s: "%s"' % (module, e)
        )
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured((
            'Module "%s" does not define a class named "%s"'
        ) % (module, attr))
    return cls


class ActivitiesConfig(AppConfig):
    name = 'activities'

    def ready(self):
        installed_notifiers = getattr(
            settings, 'ACTIVITIES_INSTALLED_NOTIFIERS', ()
        )
        for notifier in installed_notifiers:
            if isinstance(notifier, (list, tuple)):
                name = notifier[0]
                path = notifier[1]
                args = notifier[2:]
            elif isinstance(notifier, str):
                name = None
                path = notifier
                args = []
            cls = get_class(path)
            notifier_registry.register(cls(*args), name, overwrite=True)
