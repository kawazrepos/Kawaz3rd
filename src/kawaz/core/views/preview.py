#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/2
#
from django.core.exceptions import ImproperlyConfigured
__author__ = 'giginet'

class BaseObjectPreviewMixin(object):

    def get_object(self, queryset=None):
        """
        get parameterで渡ってきた値からオブジェクトを作ります
        """
        params = self.request.GET.dict()
        return params
