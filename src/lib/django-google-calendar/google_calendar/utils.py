# coding=utf-8
"""
"""

from functools import lru_cache
from importlib import import_module
from django.db.models.loading import get_model as _get_model
from django.core.exceptions import (ImproperlyConfigured,
                                    AppRegistryNotReady)


@lru_cache()
def get_model(model):
    """
    Get a model class from 'app_label.model_name' type of string
    """
    if isinstance(model, str):
        app_label, model_name = model.rsplit('.', 1)
        try:
            model = _get_model(app_label, model_name)
        except (LookupError, AppRegistryNotReady):
            return None
    return model


@lru_cache()
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
    if not isinstance(path, str):
        return path
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

# === from django-observer ==============================================


def get_relation(relation):
    """
    Resolve relation

    This function resolve a relation indicated as a string (e.g.
    'app_name.Model'). The 'relation' can be a model class for convinience.
    It return ``None`` when the relation could not be resolved. It is happend
    when the related class is not loaded yet.

    Args:
        relation (str or class): A model indicated as a string or class

    Returns:
        (None or a class, app_label, model_name)
    """
    # Try to split the relation
    try:
        app_label, model_name = relation.split('.', 1)
    except AttributeError:
        app_label = relation._meta.app_label
        model_name = relation._meta.model_name
    return app_label, model_name


_pending_lookups = {}


def resolve_relation_lazy(relation, operation, **kwargs):
    """
    Resolve relation and call the operation with the specified kwargs.

    The operation will be called when the relation is ready to resolved.
    The original idea was copied from Django 1.2.2 source code thus the
    license belongs to the Django's license (BSD License)

    Args:
        relation (str or class): A relation which you want to resolve
        operation (fn): A callback function which will called with resolved
            relation (class) and the specified kwargs.
    """
    app_label, model_name = get_relation(relation)
    try:
        model = _get_model(app_label, model_name)
        operation(model, **kwargs)
    except AppRegistryNotReady:
        key = (app_label, model_name)
        value = (operation, kwargs)
        _pending_lookups.setdefault(key, []).append(value)


def _do_pending_lookups(sender, **kwargs):
    key = (sender._meta.app_label, sender.__name__)
    for operation, kwargs in _pending_lookups.pop(key, []):
        operation(sender, **kwargs)


from django.db.models.signals import class_prepared
class_prepared.connect(_do_pending_lookups)
