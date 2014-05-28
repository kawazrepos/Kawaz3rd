# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from rest_framework import viewsets
from .filters import KawazObjectPermissionFilter


class KawazModelViewSet(viewsets.ModelViewSet):
    author_field_name = None

    def pre_save(self, obj):
        if self.author_field_name and self.request.user.is_authenticated():
            obj[self.author_field_name] = self.request.user

    def get_queryset(self):
        manager = self.model.objects
        if self.request.method == 'GET':
            return self.get_queryset_for_read(manager)
        return self.get_queryset_for_write(manager)

    def get_queryset_for_read(self, manager):
        if hasattr(manager, 'published'):
            return manager.published(self.request.user)
        return manager.all()

    def get_queryset_for_write(self, manager):
        if hasattr(manager, 'related'):
            return manager.related(self.request.user)
        return manager.all()

    def get_filter_backends(self):
        return (KawazObjectPermissionFilter,)
