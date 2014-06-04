from django import template
from django.template import TemplateSyntaxError
from ..models import Project

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_projects(context, lookup='published'):
    """
    任意の<lookup>によりフィルタされた Project のクエリを取得し指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_projects as <variable> %}
        {% get_projects <lookup> as <variable> %}

    Lookup: (Default: published)
        published: ユーザーに対して公開された Project を返す
        draft: ユーザーが編集可能な下書き Project を返す
        active: ユーザーが閲覧可能なアクティブ Project を返す

    Examples:
        公開された Project のクエリを取得し、最新5件のみを描画

        {% get_projects as projects %}
        {% for in projects|slice:":5" %}
            {{ projects }}
        {% endfor %}

        下書き記事を取得

        {% get_projects 'draft' as draft_projects %}
    """
    ALLOWED_LOOKUPS = ('published', 'draft', 'active',)
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_projects'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    # 'request' は settings.TEMPLATE_CONTEXT_PROCESSOR に
    # 'django.core.context_processors.request' が指定されていないと存在しない
    # ここでは敢えて存在しない場合にエラーを出すため直接参照している
    request = context['request']
    if lookup == 'published':
        qs = Project.objects.published(request.user)
    elif lookup == 'draft':
        qs = Project.objects.draft(request.user)
    elif lookup == 'active':
        qs = Project.objects.active(request.user)
    return qs
