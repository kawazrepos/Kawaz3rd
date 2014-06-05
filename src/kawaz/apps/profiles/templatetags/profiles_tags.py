from django import template
from django.template import TemplateSyntaxError
from ..models import Profile

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_profiles(context, lookup='published'):
    """
    任意の<lookup>によりフィルタされた Profile のクエリを取得し指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_profiles as <variable> %}
        {% get_profiles <lookup> as <variable> %}

    Lookup: (Default: published)
        published: ユーザーが閲覧可能な Profile を返す

    Examples:
        閲覧可能な Profile を取得し5件のみを描画

        {% get_profiles as profiles %}
        {% for profile in profiles|slice:":5" %}
            {{ profile }}
        {% endfor %}
    """
    ALLOWED_LOOKUPS = ('published',)
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_profiles'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    # 'request' は settings.TEMPLATE_CONTEXT_PROCESSOR に
    # 'django.core.context_processors.request' が指定されていないと存在しない
    # ここでは敢えて存在しない場合にエラーを出すため直接参照している
    request = context['request']
    if lookup == 'published':
        qs = Profile.objects.published(request.user)
    return qs
