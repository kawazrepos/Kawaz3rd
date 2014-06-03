# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = (
    'ReadModelMixin', 'WriteModelMixin',
    'CreateModelMixin', 'ListModelMixin',
    'RetrieveModelMixin', 'UpdateModelMixin',
    'DestroyModelMixin',
)
from rest_framework.mixins import CreateModelMixin as _CreateModelMixin


class ReadModelMixin(object):
    """
    A mixin for reading model objects.

    It add `get_queryset_for_read` method and override `get_queryset` method.
    """
    def get_queryset_for_read(self):
        """
        Return a queryset for reading.

        If the object manager have `published` method, this execute the method
        with `self.request.user`, otherwise it simply return all.
        """
        m = self.model.objects
        if hasattr(m, 'published'):
            return m.published(self.request.user)
        return m.all()

    def get_queryset(self):
        return self.get_queryset_for_read()


class WriteModelMixin(object):
    """
    A mixin for writing model objects.

    It add `get_queryset_for_write` method and override `get_queryset` method.
    """
    def get_queryset_for_write(self):
        """
        Return a queryset for writing.

        If the object manager have `related` method, this execute the method
        with `self.request.user`, otherwise it simply return all.
        """
        m = self.model.objects
        if hasattr(m, 'related'):
            return m.related(self.request.user)
        return m.all()

    def get_queryset(self):
        return self.get_queryset_for_write()


class ReadWriteModelMixin(ReadModelMixin, WriteModelMixin):
    """
    A mixin for reading/writing model objects.

    It add `get_queryset_for_read` method and `get_queryset_for_write` method
    and override `get_queryset` method.
    The queryset will be determined from the value of `self.request.method`.
    """

    def get_queryset(self):
        if self.request.method == 'GET':
            return self.get_queryset_for_read()
        return self.get_queryset_for_write()


class CreateModelMixin(_CreateModelMixin):
    """
    Create model instance and automatically save author
    """
    def pre_save(self, obj):
        # validation check
        if not hasattr(self, 'author_field_name'):
            raise AttributeError(
                "You need to specify 'author_field_name' as "
                "a class attribute to '{}'. "
                "If there is no author field, simply specify 'None'.".format(
                    self.__class__.__name__)
            )
        if self.author_field_name and self.request.user.is_authenticated():
            setattr(obj, self.author_field_name, self.request.user)

# Make it easy to understand, just make alias of rest_framework builtins
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
