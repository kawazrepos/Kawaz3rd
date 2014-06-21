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

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def youtube(value):
    """
    文中に含まれているYouTubeの動画URLをプレーヤーに変換します
    ただし、URLは行頭から始まっている必要があります
    これは、HTMLタグ内に含まれているURLの展開を防ぐためです
    """
    def repl(m):
        id = m.group('id')
        html = render_to_string("templatetags/youtube.html", {
            'video_id' : id
        })
        return html
    value = YOUTUBE_PATTERN.sub(repl, value)
    return mark_safe(value)

@register.filter
@template.defaultfilters.stringfilter
def nicovideo(value):
    """
    文中に含まれているニコニコ動画のURLをプレーヤーに変換します
    ただし、URLは行頭から始まっている必要があります
    これは、HTMLタグ内に含まれているURLの展開を防ぐためです
    """
    def repl(m):
        id = m.group('id')
        html = render_to_string("templatetags/nicovideo.html", {
            'video_id' : id
        })
        return html
    value = NICONICO_PATTERN.sub(repl, value)
    return mark_safe(value)
