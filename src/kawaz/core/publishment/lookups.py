# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db.models import Q


def published_lookup(user_obj, field_name='pub_state'):
    """
    Return an instance of Q object to lookup the objects which is published to
    the specified user.

    If the user is Kawaz member, the lookup return the public and protected
    objects otherwise only public objects.

    Args:
        user_obj (obj): User model instance (or AnonymousUser instance)
        field_name (str): A name of the field which represent the publishment
            status (Default: ``'pub_state'``)

    Returns:
        An instance of Q object
    """
    q = Q(**{field_name: 'public'})
    if user_obj and user_obj.is_authenticated() and user_obj.is_member:
        q |= Q(**{field_name: 'protected'})
    return q


def draft_lookup(user_obj, author_field_name='author', field_name='pub_state'):
    """
    Return an instance of Q object to lookup the draft objects of the specified
    user.

    If the user is Kawaz member, the lookup return own draft objects otherwise
    non objects.

    Args:
        user_obj (obj): User model instance (or AnonymousUser instance)
        author_field_name (str): A name of the foreign field which represent
            the author user (Default: ``'author'``)
        field_name (str): A name of the field which represent the publishment
            status (Default: ``'pub_state'``)

    Returns:
        An instance of Q object
    """
    if user_obj and user_obj.is_authenticated() and user_obj.is_member:
        q = Q(**{author_field_name: user_obj, field_name: 'draft'})
    else:
        # pk = -1 never exists
        q = Q(pk=-1)
    return q

