# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/17
#

from crispy_forms.helper import FormHelper


class Bootstrap3HorizontalFormHelper(FormHelper):
    """
    Bootstrap3のHorizontalFormを利用するためのHelperです

    Ref:
        http://django-crispy-forms.readthedocs.org/en/latest/crispy_tag_forms.html#bootstrap3-horizontal-forms
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form_class = 'form-horizontal'
        self.label_class = 'col-lg-2'
        self.field_class = 'col-lg-8'
        self.form_action = '.'


class Bootstrap3InlineFormHelper(FormHelper):
    """
     Bootstrap3のInlineFormを利用するためのHelperです

     Ref:
        http://django-crispy-forms.readthedocs.org/en/latest/crispy_tag_forms.html#bootstrap3-inline-forms
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = 'form-inline'
        self.field_template = 'bootstrap3/layout/inline_field.html'


class HorizontalBareFormHelper(Bootstrap3HorizontalFormHelper):
    """
    HorizontalFormHelperの<form>タグでwrapされていない版です
    主にget_form_helperテンプレートタグからの利用を想定しています
    form_tag = False
    """
    form_tag = False


class InlineBareFormHelper(Bootstrap3InlineFormHelper):
    """
    InlineFormHelperの<form>タグでwrapされていない版です
    主にget_form_helperテンプレートタグからの利用を想定しています
    form_tag = False
    """
    form_tag = False
