from django import template
from django.utils.safestring import mark_safe

from .embed import youtube, nicovideo
from .mention import mention

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def parse(value, full=True):
    """
    Kawazで使用するtemplate tagsをまとめて使用するtemplate filter
    """
    # URL
    if full:
        # Youtube, NicoNico
        value = youtube(value)
        value = nicovideo(value)
        # @言及
        value = mention(value)
    return mark_safe(value)