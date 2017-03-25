import re
from django import template
from django.utils.safestring import mark_safe


PATTERN = re.compile(
    r'(?:https?|ftp)://[\.\-\+\?\(\)\{\}\^\$\w\d/:;@&=,%#]+',
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
        def repl(m):
            from kawaz.core.utils.shortenurl import shorten
            return shorten(m.group())
        replaced_value = PATTERN.sub(repl, value)
        return mark_safe(replaced_value)
