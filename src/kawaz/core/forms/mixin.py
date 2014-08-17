# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/16
#
__author__ = 'giginet'
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from crispy_forms.layout import Submit
from .helpers import Bootstrap3HorizontalFormHelper, Bootstrap3InlineFormHelper


class BaseFormHelperMixin(object):
    helper_class = None
    form_tag = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.helper_class:
            raise ImproperlyConfigured("FormHelperMixin must be set `helper_class`.")
        self.helper = self.get_helper()
        self.helper.form_tag = self.form_tag

        for object in self.get_additional_objects():
            self.helper.add_input(object)

    def get_helper(self):
        return self.helper_class()

    def get_additional_objects(self):
        return (Submit('save', _("Save"),
                      css_class='btn btn-success btn-lg col-lg-offset-2 '
                                'col-xs-offset-2'),)


class Bootstrap3HorizontalFormHelperMixin(BaseFormHelperMixin):
    """
    django-crispy-formsを使って、bootstrap3対応のHorizontalFormを作成するMixinです。

    Usage:

        class ArticleForm(BootstrapHorizontalFormMixin, ModelForm):
            model = Article

    """
    helper_class = Bootstrap3HorizontalFormHelper


class Bootstrap3InlineFormHelperMixin(BaseFormHelperMixin):
    """
    django-crispy-formsを使って、bootstrap3対応のInlineFormを作成するMixinです。
    """
    helper_class = Bootstrap3InlineFormHelper
