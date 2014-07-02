#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/2
#
from django.core.exceptions import ImproperlyConfigured
__author__ = 'giginet'

class BaseObjectPreviewMixin(object):
    global_ignore_fields = ['csrfmiddlewaretoken',]
    ignore_fields = []

    def get_object(self, queryset=None):
        """
        get parameterで渡ってきた値からオブジェクトを作ります
        """

        if not self.model:
            raise ImproperlyConfigured("%(cls)s is missing a queryset. Define "
                                       "%(cls)s.model, %(cls)s.queryset, or override "
                                       "%(cls)s.get_queryset()." % {
                                           'cls': self.__class__.__name__
                                       })
        params = self.request.GET.dict()
        for ignore in (self.ignore_fields + self.global_ignore_fields):
            del params[ignore]
        obj = self.model(**params)
        obj.save(commit=False)
        return obj

