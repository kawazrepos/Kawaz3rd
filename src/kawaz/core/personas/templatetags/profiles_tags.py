__author__ = 'giginet'

from django import template
from django.template import TemplateSyntaxError
from ..models import Profile

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_my_profile(context):
    """
    現在のログインユーザーのプロフィールを取り出すテンプレートタグ
    セキュリティの観点から、任意のユーザーのプロフィール情報を取り出すことはできず、
    必ずログインユーザーの物が返される
    もし、ログインユーザーがプロフィールを持っていなかったり（wille）、
    渡されたユーザーが非ログインユーザーだった場合は`None`を返す

    Example:
        {% load profiles_tags %}
        {% get_my_profile as profile %}
        {{ profile.remarks }}
    """
    user = context.get('user', None)
    if not user:
        return None
    return getattr(user, '_profile', None)
