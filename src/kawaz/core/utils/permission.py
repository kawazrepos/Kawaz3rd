# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


def get_full_permission_name(codename, obj):
    """
    Return permission string from codename and model

    Args:
        codename (str): A codename of the permission (e.g. 'add')
        obj (instance): An instance of model
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.object_name.lower()
    perm = '{}.{}_{}'.format(app_label, codename, model_name)
    return perm
