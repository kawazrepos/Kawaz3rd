# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/16
#
__author__ = 'giginet'

from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

class Bootstrap3HorizontalFormMixin(object):
    """
    django-crispy-formsを使って、bootstrap3対応のform layoutを作成するMixinです。

    Ref:
        http://django-crispy-forms.readthedocs.org/en/latest/crispy_tag_forms.html#bootstrap3-horizontal-forms

    Usage:

        class ArticleForm(BootstrapHorizontalFormMixin, ModelForm):
            model = Article

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = '.'
        self.helper.add_input(self.get_submit())

    def get_submit(self):
        return Submit('save', _("Save"),
                      css_class='btn btn-success btn-lg col-lg-offset-2')
