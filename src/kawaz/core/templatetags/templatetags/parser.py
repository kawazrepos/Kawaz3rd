from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import urlize

from .embed import youtube, nicovideo
from .mention import mention

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def parser(value):
    """
    Kawazで使用するtemplate tagsをまとめて使用するtemplate filterです
    以下の処理を行います
        YouTube展開
        ニコニコ動画展開
        URLをリンクに展開
        @usernameを展開
    """
    # URL
    # Youtube, NicoNico
    value = youtube(value)
    value = nicovideo(value)
    # URL
    value = urlize(value)
    # @言及
    value = mention(value)
    return mark_safe(value)