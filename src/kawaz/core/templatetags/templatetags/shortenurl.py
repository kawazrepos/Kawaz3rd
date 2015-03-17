import re
from django import template
from django.utils.safestring import mark_safe
from kawaz.core.utils.shortenurl import shorten

__author__ = 'giginet'

PATTERN = re.compile(
    r'(https?|ftp)(:\/\/[-_.!~*()a-zA-Z0-9;\/?:\@&=+\$,%#]+)',
    flags=re.MULTILINE,
)

register = template.Library()

@register.tag('shortenurl')
def do_shortenurl(parser, token):
    """
    ブロックで囲まれたテキストに含まれるURLを短縮するテンプレートタグ

    Usage:
        {% shortenurl %}
        Kawazポータルです http://www.kawaz.org/
        {% endshortenurl %}
    """
    ENDMARKER = "end" + token.split_contents()[0]
    nodelist = parser.parse(ENDMARKER)
    parser.delete_first_token()
    return ShortenURLNode(nodelist)

class ShortenURLNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        value = self.nodelist.render(context)
        replaced_value = PATTERN.sub(shorten, value)
        return mark_safe(replaced_value)
