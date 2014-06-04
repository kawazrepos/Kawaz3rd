from django import template
from django.template import TemplateSyntaxError
from ..models import Star

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_stars(context, lookup='published'):
    """
    任意の<lookup>によりフィルタされた Star のクエリを取得し指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_stars as <variable> %}
        {% get_stars <lookup> as <variable> %}

    Lookup: (Default: published)
        published: ユーザーに対して公開された Star を返す

    Examples:
        公開された Star のクエリを取得し、最新5件のみを描画

        {% get_stars as stars %}
        {% for in stars|slice:":5" %}
            {{ stars }}
        {% endfor %}

    """
    ALLOWED_LOOKUPS = ('published',)
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_stars'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    # 'request' は settings.TEMPLATE_CONTEXT_PROCESSOR に
    # 'django.core.context_processors.request' が指定されていないと存在しない
    # ここでは敢えて存在しない場合にエラーを出すため直接参照している
    request = context['request']
    if lookup == 'published':
        qs = Star.objects.published(request.user)
    return qs
