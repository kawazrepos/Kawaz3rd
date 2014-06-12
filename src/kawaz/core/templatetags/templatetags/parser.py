from django import template
from django.utils.safestring import mark_safe

from .viewer import youtube, nicovideo

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def parse(value, full=True):
    """
    Kawazで使用するtemplate tagsをまとめて使用するtemplate filter
    :param value:
    :param full:
    :return:
    """
    # URL
    if full:
        # Youtube, NicoNico
        value = youtube(value)
        value = nicovideo(value)
    return mark_safe(value)