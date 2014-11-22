# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import re
from django import template


NEWLINE_PATTERN = re.compile("(?:\r\n)|\r|\n", re.MULTILINE)
register = template.Library()


@register.filter('strip_newlines')
@template.defaultfilters.stringfilter
def strip_newlines(value, repl=''):
    """
    指定されたテキストから改行文字を取り除くテンプレートフィルタ

    Usage:
        {{ object.body | strip_newlines }}
        {{ object.body | strip_newlines:' ' }}  # 半角スペースに置換

    """
    value = NEWLINE_PATTERN.sub(repl, value)
    return value
