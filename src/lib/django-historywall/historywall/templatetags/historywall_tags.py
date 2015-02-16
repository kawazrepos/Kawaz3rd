# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django import template
from django.template.loader import select_template
from django.utils.safestring import mark_safe
from ..models import Wall


register = template.Library()


def get_template_names(wall, prefix='', suffix='', ext='.html'):
    """
    Get a list of template name used to render the wall
    """
    ct = wall.content_type
    app_label = ct.app_label
    model_name = ct.model.__name__.lower()
    return (
        "historywall/{}/{}{}{}{}".format(
            app_label, prefix, model_name, suffix, ext),
        "historywall/{}{}{}{}".format(
            prefix, app_label, suffix, ext),
    )


@register.simple_tag(takes_context=True)
def render_wall(context, wall):
    """
    Render an instance of wall

    Usage:
        {% render_wall <wall> %}

    """
    template_names = get_template_names(wall, suffix='_wall')
    template = select_template(template_names)
    context.push()
    context.update(dict(
        wall=wall,
        object=wall.content_object,
    ))
    rendered = template.render(context)
    context.pop()
    return mark_safe(rendered)


@register.simple_tag(takes_context=True)
def render_history(context, history):
    """
    Render an instance of history

    Usage:
        {% render_history <history> %}

    """
    template_names = get_template_names(history.wall, suffix='_history')
    template = select_template(template_names)
    context.push()
    context.update(dict(
        wall=history.wall,
        history=history,
        object=history.wall.content_object,
    ))
    rendered = template.render(context)
    context.pop()
    return mark_safe(rendered)


@register.assignment_tag
def get_walls():
    """
    Get a queryset of walls

    Usage:
        {% get_walls as <variable> %}
    """
    return Wall.objects.all()

