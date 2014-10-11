from django import template
from ..models import HatenablogEntry

register = template.Library()


@register.assignment_tag
def get_hatenablog_entries():
    """
    Hatenablog 更新情報を指定された <variable> に格納

    Syntax:
        {% get_hatenablog_entries as <variable> %}

    Example:
        最近更新された Hatenablog の記事を5つ描画

        {% get_hatenablog_entries as entries %}
        {% for entry in entries|slice:":5" %}
            {{ entry }}
        {% endfor %}
    """
    return HatenablogEntry.objects.all()
