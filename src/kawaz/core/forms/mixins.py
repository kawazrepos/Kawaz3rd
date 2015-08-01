# ! -*- coding: utf-8 -*-
#
#
#

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Submit
from .helpers import Bootstrap3HorizontalFormHelper, Bootstrap3InlineFormHelper


class FormHelperMixinBase(object):
    helper_class = None
    form_tag = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.helper_class:
            raise ImproperlyConfigured("helper_class attribute is required to be specified.")
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


class Bootstrap3HorizontalFormHelperMixin(FormHelperMixinBase):
    """
    django-crispy-formsを使って、bootstrap3対応のHorizontalFormを作成するMixinです。

    Usage:

        class ArticleForm(BootstrapHorizontalFormMixin, ModelForm):
            model = Article

    """
    helper_class = Bootstrap3HorizontalFormHelper


class Bootstrap3InlineFormHelperMixin(FormHelperMixinBase):
    """
    django-crispy-formsを使って、bootstrap3対応のInlineFormを作成するMixinです。
    """
    helper_class = Bootstrap3InlineFormHelper
