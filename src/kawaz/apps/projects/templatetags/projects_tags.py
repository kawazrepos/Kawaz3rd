from django import template
from django.template import TemplateSyntaxError
from ..models import Project
from django.db.models import Count

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
        active: ユーザーが閲覧可能なactiveな Project を返す
        recently_planned: ユーザーが閲覧可能な直近90日以内に作られた企画中な Project を返す
        archived: 以下の条件を満たすプロジェクトを返す
            状態が一時停止中、エターナった、完成済み、もしくは
            企画中であるが、作成から90日以上経過している

    Examples:
        公開された Project のクエリを取得し、最新5件のみを描画

        {% get_projects as projects %}
        {% for project in projects|slice:":5" %}
            {{ project }}
        {% endfor %}

        下書き記事を取得

        {% get_projects 'draft' as draft_projects %}
    """
    ALLOWED_LOOKUPS = ('published', 'draft', 'active', 'recently_planned', 'archived')
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
    elif lookup == 'recently_planned':
        qs = Project.objects.recently_planned(request.user)
    elif lookup == 'archived':
        qs = Project.objects.archived(request.user)

    return qs.prefetch_related('members').annotate(members_count=Count('members'))

@register.assignment_tag(takes_context=True)
def get_published_joined_projects_of(context, user):
    """
    userがメンバーに含まれているプロジェクト一覧を返します

    Syntax:
        {% get_published_joined_projects_of user %}
    """
    qs = get_projects(context)
    return qs.filter(members__in=user)

