# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'

import os
from itertools import chain
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.forms import RadioSelect
from django.forms.widgets import RadioFieldRenderer
from django.utils.safestring import mark_safe


class RadioWithHelpTextFieldRenderer(RadioFieldRenderer):
    # Ref: https://djangosnippets.org/snippets/2146/
    def __init__(self, name, value, attrs, choices, help_texts):
        self.help_texts = help_texts
        super().__init__(name, value, attrs, choices)

    def render(self):
        listitems = []
        basehtml = "<li>{}<br><small>{}</small></li>"
        for ori, help_text in zip(self, self.help_texts):
            listitems.append(basehtml.format(ori, help_text))
        return mark_safe("<ul>\n{}\n</ul>".format("\n".join(listitems)))


class RadioSelectWithHelpText(RadioSelect):
    """
    RadioSelect with help texts
    """
    # Ref: https://djangosnippets.org/snippets/2146/
    renderer = RadioWithHelpTextFieldRenderer

    def __init__(self, *args, **kwargs):
        self.help_texts = kwargs.pop('help_texts', [])
        super().__init__(*args, **kwargs)

    def get_renderer(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ""

        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        help_texts = self.help_texts
        return self.renderer(name, value, final_attrs,
                             choices, help_texts)


class MaceEditorWidget(widgets.Textarea):
    """
    Markdownエディタを組み込むためのWidgetです
    """

    def __init__(self):
        super().__init__(attrs={'class': 'mace-editor'})

    def render(self, name, value, attrs=None):
        area = super().render(name, value, attrs)
        template = render_to_string(os.path.join("components", "mace-header.html"))
        return area + mark_safe(template)

    class Media:
        js = ('vendor/mace.min.js', 'js/editor.js',)
