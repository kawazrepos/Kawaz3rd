# coding=utf-8
"""
"""

from rest_framework import filters
from kawaz.core.utils.permission import filter_with_perm


class KawazObjectPermissionFilterBackend(filters.BaseFilterBackend):
    """
    A filter backend that limits results to those where the requesting user
    has read object level permissions.
    """
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if request.method == 'GET':
            queryset = filter_with_perm(user, queryset, 'view')
        return queryset
