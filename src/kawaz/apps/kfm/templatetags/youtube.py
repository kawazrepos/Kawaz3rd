# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django import template
from django.utils.safestring import mark_safe
from ..extras.youtube import parse_youtube_urls


register = template.Library()


@register.filter('youtube')
@template.defaultfilters.stringfilter
def filter_youtube(value, size=None):
    """
    指定されたテキスト内に存在するYouTube URLを展開するフィルタ

    Usage:
        {{ object.body | youtube }}
        {{ object.body | youtube:'responsive' }}    # レスポンシブデザイン
        {{ object.body | youtube:'1600' }}          # 横幅指定（16:9）
        {{ object.body | youtube:'1600,900' }}      # 縦横幅指定

    """
    width = None
    height = None
    responsive = False
    if size == 'responsive':
        responsive = True
    elif size:
        bits = size.split(',', 1)
        if len(bits) == 1:
            width = int(bits[0])
        else:
            width = int(bits[0])
            height = int(bits[1])
    value = parse_youtube_urls(value,
                               responsive=responsive,
                               width=width, height=height)
    return mark_safe(value)


