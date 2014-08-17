# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/17
#
__author__ = 'giginet'

from django import template
from django.template import TemplateSyntaxError
from ..helpers import Bootstrap3HorizontalFormHelper

register = template.Library()


@register.assignment_tag
def get_form_helper(type='horizontal'):
    """
    <type>に応じたFormHelperを返します。
    もし、該当する<type>が見つからない場合は、TemplateSyntaxErrorを投げます。

    Syntax:
        {% get_form_helper as <variable> %}
        {% get_form_helper <type> as <variable> %}

    Type: (Default: horizontal)
        horizontal: Bootstrap3のHorizontal Formを描画するHelper

    Examples:
        任意のFormに対してHorizontalFormHelperを適応する
        {% load crispy_form_tags %}
        {% load form_helper %}

        {% get_form_helper "horizontal" as helper %}
        {% crispy form helper %}
    """
    if type == 'horizontal':
        return Bootstrap3HorizontalFormHelper()
    raise TemplateSyntaxError('{} is invalid form helper type.'.format(type))