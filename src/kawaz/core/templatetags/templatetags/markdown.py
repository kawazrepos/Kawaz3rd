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
    """
    テキストをmarkdownに展開するtemplate filterです。
    processorとしてpython-markdown2を使っており、デフォルトの挙動の他に以下のExtrasを含めています

    Extras:
        footnotes
            https://github.com/trentm/python-markdown2/wiki/footnotes
            geekdrums [^foot-note]
            [^foot-note]: 神、いわゆるゴッド
        code-friendly
            https://github.com/trentm/python-markdown2/wiki/code-friendly
            _hello_, __yo__ などと言った記法を無効化します

    Usage:
        {% load markdown %}
        {{ object.body | markdown }}
    """
    md = markdown2.markdown(value, extras=['footnotes',
                                           'code-friendly'],
    )
    return mark_safe(md)