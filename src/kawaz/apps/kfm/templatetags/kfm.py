# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from ..parser import parse_kfm


register = template.Library()


@register.simple_tag(takes_context=True)
def include_kfm(context, template_path):
    """
    テンプレートフォルダに存在する Kawaz Flavored Markdown ファイルを読み込み
    レンダリングするテンプレートタグ

    Usage:
        {% include_kfm "markdown/about.md" %}

    """
    template_path = template.resolve_variable(template_path, context)
    value = render_to_string(template_path)
    return mark_safe(parse_kfm(value))


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
