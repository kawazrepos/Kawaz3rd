# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import lru_cache
from importlib import import_module
from django.core.exceptions import ImproperlyConfigured


@lru_cache
def get_model(model):
    """
    Get a model class from 'app_label.model_name' type of string
    """
    if isinstance(model, str):
        app_label, model_name = model.rsplit('.', 1)
        model = get_model(app_label, model_name)
    return model


@lru_cache
def get_class(path):
    """
    Return a class of a given the dotted Python import path (as a string).

    If the addition cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    """
    if not path:
        return None
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(
                'Error loading a module %s: "%s"' % (module, e))
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured((
                'Module "%s" does not define a class named "%s"'
        ) % (module, attr))
    return cls
