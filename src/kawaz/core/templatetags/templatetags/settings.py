from django import template
from django.conf import settings as _settings

__author__ = 'giginet'

register = template.Library()


@register.simple_tag
def settings(name):
    return str(getattr(_settings, name, ''))
