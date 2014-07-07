__author__ = 'giginet'
import re
import markdown2
from django import template
from django.utils.safestring import mark_safe

# Ref https://github.com/trentm/python-markdown2/wiki/link-patterns
LINK_PATTERNS = [(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def markdown(value):
    md = markdown2.markdown(value, extras=['footnotes',
                                           'markdown-in-html'],
    )
    return mark_safe(md)