import re
from django.template.loader import render_to_string
from .utils import is_quoated


PATTERN = re.compile(
    r'(?:https?|ftp)://[\.\-\+\?\(\)\{\}\^\$\w\d/:;@&=,%#]+',
    flags=re.MULTILINE,
)
TEMPLATE_NAME = 'kfm/extras/autolink.html'


def parse_autolinks(value):
    """
    指定された文字列から装飾されていないURLを探しリンク展開する
    """
    def repl(m):
        if is_quoated(m.string, m.start(), m.end()):
            # クォートされているので無視
            return m.group()
        html = render_to_string(TEMPLATE_NAME, {
            'url': m.group(),
        })
        return html.strip()
    value = PATTERN.sub(repl, value)
    return value
