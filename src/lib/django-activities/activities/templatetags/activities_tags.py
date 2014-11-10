# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django import template
from django.template import TemplateSyntaxError
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from ..models import Activity
from ..registry import registry


register = template.Library()


class RenderActivityNode(template.Node):
    def __init__(self, activity, typename=None):
        self.activity = template.Variable(activity)
        self.typename = template.Variable(typename) if typename else None

    def render(self, context):
        activity = self.activity.resolve(context)
        # get activity mediator instance connected to a model which the
        # activity target to
        mediator = registry.get(activity)
        # render activity instance via render method of a corresponding
        # mediator
        if self.typename:
            typename = self.typename.resolve(context)
        else:
            typename = None
        context.push()
        rendered = mediator.render(activity, context, typename=typename)
        context.pop()
        return mark_safe(rendered)


@register.tag
def render_activity(parser, token):
    """
    Render an instance of Activity via 'render' method of a
    corresponding activity mediator of a model which the activity target to.
    <typename> is used to specify a way of rendering

    Usage:
        {% render_activity <activity> %}
        {% render_activity <activity> of <typename> %}

    """
    bits = token.split_contents()
    if len(bits) == 4:
        if bits[2] != 'of':
            raise TemplateSyntaxError(
                "second argument of {} tag must be 'of'".format(bits[0])
            )
        return RenderActivityNode(bits[1], bits[3])
    elif len(bits) == 2:
        return RenderActivityNode(bits[1])
    raise TemplateSyntaxError("{} tag takes exactly 2 or 4 arguments.")


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

@register.assignment_tag
def get_activities_of(model_or_object):
    """
    Get a queryset of activities which related to the specified model (string)
    or object.

    Usage:
        {% get_activities_of <model> as <variable> %}
        {% get_activities_of '<app_label>.<model_name>' as <variable> %}

    Example:
        {# Get activities related to the 'object' #}
        {% get_activities_of object as activities %}

        {# Get activities related to the 'events.Event' model #}
        {% get_activities_of 'events.Event' as activities %}

    """
    if isinstance(model_or_object, str):
        app_label, model_name = model_or_object.split('.', 1)
        ct = ContentType.objects.get_by_natural_key(
            app_label.lower(),
            model_name.lower(),
        )
        return Activity.objects.get_for_model(ct.model_class())
    else:
        return Activity.objects.get_for_object(model_or_object)

