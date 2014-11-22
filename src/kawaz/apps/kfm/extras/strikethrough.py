# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import re
from .utils import is_quoated


STRIKETHROUGH_PATTERN = re.compile("~~(?P<text>[^~]+)~~", re.MULTILINE)


def parse_strikethroughs(value):
    """
    ~~で囲まれた部分を<del>展開する
    """
    def repl(m):
        if is_quoated(m.string, m.start(), m.end()):
            return m.group()
        return "<del>{}</del>".format(m.group('text'))
    return STRIKETHROUGH_PATTERN.sub(repl, value)
