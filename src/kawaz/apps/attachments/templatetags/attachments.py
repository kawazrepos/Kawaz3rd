# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/9/23
#
__author__ = 'giginet'

from django import template
from django.utils.safestring import mark_safe
from ..models import Material
import re

register = template.Library()

COMMONS_PATTERN = re.compile(r"\{attachments:\W*(?P<slug>[^}:]+)\W*\}", re.MULTILINE)

@register.filter
@template.defaultfilters.stringfilter
def parse_attachments(value):
    """
    {attachments:47c833254e45532d850cc40a0b8ec8b055b27c71}的なタグをparseします

    Usage
        {{ <value>|parse_attachments }}

    """
    def repl(m):
        try:
            material = Material.objects.get(slug=m.group('slug'))
            preview_html = material.get_thumbnail_display()
            return preview_html
        except Material.DoesNotExist:
            return m.group(0)
    value = re.sub(COMMONS_PATTERN, repl, value)
    return mark_safe(value)

