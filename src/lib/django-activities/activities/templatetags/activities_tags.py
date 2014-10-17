# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django import template
from django.template import TemplateSyntaxError
from django.utils.safestring import mark_safe
from ..models import Activity
from ..registry import registry


register = template.Library()


@register.simple_tag(takes_context=True)
def render_activity(context, activity):
    """
    Render an instance of Activity via 'render' method of a
    corresponding activity mediator of a model which the activity target to

    Usage:
        {% render_activity <activity> %}

    """
    # get activity mediator instance connected to a model which the
    # activity target to
    mediator = registry.get(activity)
    # render activity instance via render method of a corresponding
    # mediator
    rendered = mediator.render(activity, context)
    return mark_safe(rendered)


@register.assignment_tag
def get_activities():
    """
    Get a queryset of activities

    Usage:
        {% get_activities as <variable> %}
    """
    return Activity.objects.all()


@register.assignment_tag
def get_latest_activities():
    """
    Get a queryset of latest activities of each particular content_objects

    Usage:
        {% get_latest_activities as <variable> %}
    """
    return Activity.objects.latests()
