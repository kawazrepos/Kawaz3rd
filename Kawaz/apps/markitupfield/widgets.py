# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.safestring import mark_safe

from markupfield.widgets import MarkupTextarea as _MarkupTextarea

import os.path

class MarkItUpTextarea(_MarkupTextarea):
    u"""Textarea widget render with 'jquery.markitup.js'"""
    
    def __init__(self, attrs=None,
                 markitup_set=None,
                 markitup_skin=None):
        self.miu_set = markitup_set or settings.MARKITUP_SET
        self.miu_skin = markitup_skin or settings.MARKITUP_SKIN
        if not attrs:
            attrs = {'class': 'django-markitupfield'}
        else:
            attrs['class'] = 'django-markitupfield' + " %s" % attrs['class'] if 'class' in attrs else '' 
        super(MarkItUpTextarea, self).__init__(attrs=attrs)
    
    def _media(self):
        return forms.Media(
            css={'screen': (
                '%s/style.css'%self.miu_set,
                '%s/style.css'%self.miu_skin,
            )},
            js=(
#                settings.JQUERY_PATH,
                settings.MARKITUP_SCRIPT_PATH,
                '%s/set.js'%self.miu_set,
                settings.MARKITUPFIELD_SCRIPT_PATH,
            )
        )
    media = property(_media)
    
    def render(self, name, value, attrs=None):
        html = super(MarkItUpTextarea, self).render(name, value, attrs)
        return mark_safe(html)
    
class AdminMarkItUpTextareaWidget(MarkItUpTextarea, AdminTextareaWidget):
    pass