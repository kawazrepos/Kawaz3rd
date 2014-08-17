# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/16
#
__author__ = 'giginet'
from .helpers import Bootstrap3HorizontalFormHelper

class Bootstrap3HorizontalFormMixin(object):
    """
    django-crispy-formsを使って、bootstrap3対応のform layoutを作成するMixinです。

    Usage:

        class ArticleForm(BootstrapHorizontalFormMixin, ModelForm):
            model = Article

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = Bootstrap3HorizontalFormHelper()
