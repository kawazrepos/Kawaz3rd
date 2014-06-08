#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/9
#
__author__ = 'giginet'
import re
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

YOUTUBE_PATTERN = r"""^http[s]:\/\/www.youtube.com\/watch\?v=(?P<id>[a-zA-Z0-9_-]+)$"""
NICONICO_PATTERN = r"""^http:/\/\www.nicovideo.jp\/watch\/(?P<id>[a-z]{2}[0-9]+)\/?$"""

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def youtube(value):
    """
    文中に含まれているYouTubeの動画URLをプレーヤーに変換します
    ただし、URLは行頭から始まっている必要があります
    """
    def repl(m):
        id = m.group('id')
        html = render_to_string("templatetags/youtube.html", {
            'video_id' : id
        })
        return html
    regex = re.compile(YOUTUBE_PATTERN, flags=re.MULTILINE)
    value = regex.sub(repl, value)
    return mark_safe(value)

@register.filter
@template.defaultfilters.stringfilter
def nicovideo(value):
    """
    文中に含まれているニコニコ動画のURLをプレーヤーに変換します
    ただし、URLは行頭から始まっている必要があります
    """
    def repl(m):
        id = m.group('id')
        html = render_to_string("templatetags/nicovideo.html", {
            'video_id' : id
        })
        return html
    regex = re.compile(NICONICO_PATTERN, flags=re.MULTILINE)
    value = regex.sub(repl, value)
    return mark_safe(value)
