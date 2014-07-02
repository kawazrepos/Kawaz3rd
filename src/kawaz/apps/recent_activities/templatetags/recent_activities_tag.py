from django import template
from django.template import TemplateSyntaxError
from ..models import RecentActivity

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_recent_activities(context):
    """
    RecentActivity のクエリを取得し、指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_recent_activities as <variable> %}

    Examples:
        公開された RecentActivity のクエリを取得し、最新5件のみを描画

        {% get_recent_activities as activities %}
        {% for activity in activities|slice:":5" %}
            {{ activity }}
        {% endfor %}
    """
    return RecentActivity.objects.all()
