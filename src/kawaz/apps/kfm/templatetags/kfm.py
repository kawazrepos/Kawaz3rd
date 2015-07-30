# coding=utf-8
"""
"""

from functools import wraps
from django import template
from django.utils.safestring import mark_safe
from django.template.loader_tags import do_include
from ..parser import parse_kfm


register = template.Library()


@register.tag('include_kfm')
def do_include_kfm(parser, token):
    """
    テンプレートフォルダに存在する Kawaz Flavored Markdown ファイルを読み込み
    レンダリングするテンプレートタグ

    Usage:

        {% include_kfm "markdown/about.md" %}

    """
    def parse_kfm_decorator(fn):
        @wraps(fn)
        def render(*args, **kwargs):
            rendered = fn(*args, **kwargs)
            return parse_kfm(rendered)
        return render
    node = do_include(parser, token)
    node.render = parse_kfm_decorator(node.render)
    return node


@register.filter('kfm')
@template.defaultfilters.stringfilter
def filter_kfm(value):
    """
    指定されたテキストを Kawaz Flavored Markdown として HTML 展開するフィルタ

    Usage:
        {{ object.body | kfm }}

    """
    value = parse_kfm(value)
    return mark_safe(value)


@register.tag('kfm')
def do_kfm(parser, token):
    """
    ブロックで囲まれたテキストを Kawaz Flavored Markdown として
    HTML展開するタグ

    Usage:
        {% kfm %}
        **Kawaz Flavored Markdown**
        {% endkfm %}
    """
    ENDMARKER = "end" + token.split_contents()[0]
    nodelist = parser.parse(ENDMARKER)
    parser.delete_first_token()
    return KFMNode(nodelist)


class KFMNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        value = self.nodelist.render(context)
        value = parse_kfm(value)
        return mark_safe(value)
