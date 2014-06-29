#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/9
#
__author__ = 'giginet'
import re
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

YOUTUBE_PATTERN = re.compile(r"^https?:\/\/www.youtube.com\/watch\?v=(?P<id>[a-zA-Z0-9_-]+)$", flags=re.MULTILINE)
NICONICO_PATTERN = re.compile(r"^http:/\/\www.nicovideo.jp\/watch\/(?P<id>[a-z]{2}[0-9]+)\/?$", flags=re.MULTILINE)
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
ASPECT_RATIO = 9.0 / 16.0

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def youtube(value, size=None):
    """
    文中に含まれているYouTubeの動画URLをプレーヤーに変換します
    ただし、URL以外の文字列を同じ行に含んではいけません
    これは、プレイヤーの埋め込みという性質上の仕様です

    Example:
        {{ url | youtube }}
        {{ url | youtube:'1600' }}
        {{ url | youtube:'1600,900' }}

    """
    if not size:
        width = None
        height =  None
    else:
        bits = size.split(',')
        if len(bits) == 1:
            width = bits[0]
            height = None
        elif len(bits) == 2:
            width, height = bits
    if not width and not height:
        width = DEFAULT_WIDTH
        height = DEFAULT_HEIGHT
    elif not height:
        height = int(int(width) * ASPECT_RATIO)

    def repl(m):
        id = m.group('id')
        html = render_to_string("templatetags/youtube.html", {
            'video_id' : id,
            'width': width,
            'height': height
        }).replace('\n', '')
        return html
    value = YOUTUBE_PATTERN.sub(repl, value)
    return mark_safe(value)

@register.filter
@template.defaultfilters.stringfilter
def nicovideo(value):
    """
    文中に含まれているニコニコ動画のURLをプレーヤーに変換します
    ただし、URL以外の文字列を同じ行に含んではいけません
    これは、プレイヤーの埋め込みという性質上の仕様です
    """
    def repl(m):
        id = m.group('id')
        html = render_to_string("templatetags/nicovideo.html", {
            'video_id' : id
        }).replace('\n', '')
        return html
    value = NICONICO_PATTERN.sub(repl, value)
    return mark_safe(value)
