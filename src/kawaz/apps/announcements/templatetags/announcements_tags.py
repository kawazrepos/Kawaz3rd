# coding=utf-8
"""
django templatetags for announcements app
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django import template
from django.db.models import Q
from django.template import TemplateSyntaxError
from ..models import Announcement

register = template.Library()


@register.assignment_tag
def get_announcements(lookup=None):
    """
    Put ordered queryset of announcements model into variable
    
    Syntax:
        {% get_announcements as <variable> %}
        {% get_announcements <lookup> as <variable> %}

    Lookup:
        None: Include public and protected announcements
        public: Include public announcements
        protected: Include protected announcements
        draft: Include draft announcements

    Examples:
        Put announcements queryset into 'announcements' variable and iter the
        most recent 5 instances.

        {% get_announcements as announcements %}
        {% for in announcements|slice:":5" %}
            {{ announcements }}
        {% endfor %}

        Put protected announcements queryset into 'protected_announcements'
        variable.

        {% get_announcements 'protected' as protected_announcements %}
    """
    ALLOWED_LOOKUPS = (None, 'public', 'protected', 'draft')
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_announcements'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    if lookup is None:
        qs = Announcement.objects.filter(pub_state__in=('public', 'protected'))
    elif lookup == 'public':
        qs = Announcement.objects.filter(pub_state='public')
    elif lookup == 'protected':
        qs = Announcement.objects.filter(pub_state='protected')
    elif lookup == 'draft':
        qs = Announcement.objects.filter(pub_state='draft')
    return qs.order_by('-created_at')
