from django import template
from django.template import TemplateSyntaxError
from ..models import Event

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_events(context, lookup='published'):
    """
    任意の<lookup>によりフィルタされた Event のクエリを取得し指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_events as <variable> %}
        {% get_events <lookup> as <variable> %}

    Lookup: (Default: published)
        published: ユーザーに対して公開された Event を返す
        draft: ユーザーが編集可能な下書き Event を返す
        active: ユーザーが閲覧可能な非終了 Event を返す
        attendable: ユーザーが参加可能な Event を返す

    Examples:
        公開された Event のクエリを取得し、最新5件のみを描画

        {% get_events as events %}
        {% for event in events|slice:":5" %}
            {{ event }}
        {% endfor %}

        下書き記事を取得

        {% get_events 'draft' as draft_events %}
    """
    ALLOWED_LOOKUPS = ('published', 'draft', 'active', 'attendable')
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_events'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    # 'request' は settings.TEMPLATE_CONTEXT_PROCESSOR に
    # 'django.core.context_processors.request' が指定されていないと存在しない
    # ここでは敢えて存在しない場合にエラーを出すため直接参照している
    request = context['request']
    if lookup == 'published':
        qs = Event.objects.published(request.user)
    elif lookup == 'draft':
        qs = Event.objects.draft(request.user)
    elif lookup == 'active':
        qs = Event.objects.active(request.user)
    elif lookup == 'attendable':
        qs = Event.objects.attendable(request.user)
    return qs


class Archive:
    def __init__(self, date, object_list, count):
        self.date = date
        self.object_list = object_list
        self.count = count


@register.assignment_tag(takes_context=True)
def get_monthly_archives(context):
    """
    Eventの月間アーカイブを取得する

    Usage:
        get_monthly_archive as <variable>
    """
    qs = Event.objects.all()
    date_list = qs.datetimes('period_start', 'month', order='DESC')

    archives = []
    for date in date_list:
        object_list = qs.filter(**{'period_start__year': date.year}).filter(**{'period_start__month': date.month})
        archives.append(Archive(date, object_list, object_list.count()))
    return archives
