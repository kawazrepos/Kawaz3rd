# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
from django.utils.safestring import mark_safe
from markupfield.fields import MarkupField as _MarkupField

from . import widgets

class MarkItUpField(_MarkupField):
    def __init__(self, *args, **kwargs):
        if not 'help_text' in kwargs:
            kwargs['help_text'] = mark_safe(u"""この部分には<a href="/projects/kawaz/wikis/Markdown%E3%81%AE%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95/">Markdown記法</a>を使用してマークアップを書くことができます。また通常のエディタと同じように<em>[Tab]</em>によるインデントや<em>[Shift]+[Tab]</em>によるアンインデントが利用できます。""")
        if not 'default_markup_type' in kwargs:
            kwargs['default_markup_type'] = 'html'
        super(MarkItUpField, self).__init__(*args, **kwargs)
        
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.MarkItUpTextarea}
        defaults.update(kwargs)
        return super(MarkItUpField, self).formfield(**defaults)

#from south.modelsinspector import add_introspection_rules
#add_introspection_rules([], [r"^Kawaz.markitupfield.models.MarkItUpField"])

# register MarkItUpField to use the custom widget in the Admin
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
FORMFIELD_FOR_DBFIELD_DEFAULTS[MarkItUpField] = {'widget': widgets.AdminMarkItUpTextareaWidget}