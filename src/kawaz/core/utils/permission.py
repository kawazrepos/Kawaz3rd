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


def filter_with_perm(user_obj, qs, perm):
    """
    Filter the queryset or list of object with object permission

    Args:
        user_obj (obj): An instance of User model
        qs (obj): An instance of QuerySet or list of object
        perm (string): A name of the permission（e.g. 'add'）

    Returns:

    """
    perm = get_full_permission_name(perm, qs.model)
    iterator = qs if isinstance(qs, (list, tuple)) else qs.iterator()
    iterator = filter(lambda x: user_obj.has_perm(perm, obj=x), iterator)
    return iterator
