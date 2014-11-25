from django import template
from django.template import TemplateSyntaxError
from django.utils import timezone
from ..models import Announcement

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_announcements(context, lookup='published'):
    """
    任意の<lookup>によりフィルタされた Announcement のクエリを取得し指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_announcements as <variable> %}
        {% get_announcements <lookup> as <variable> %}

    Lookup: (Default: published)
        published: ユーザーに対して公開された Announcement を返す
        draft: ユーザーが編集可能な下書き Announcement を返す

    Examples:
        公開された Announcement のクエリを取得し、最新5件のみを描画

        {% get_announcements as announcements %}
        {% for announcement in announcements|slice:":5" %}
            {{ announcement }}
        {% endfor %}

        下書き記事を取得

        {% get_announcements 'draft' as draft_announcements %}
    """
    ALLOWED_LOOKUPS = ('published', 'draft')
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_announcements'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    # 'request' は settings.TEMPLATE_CONTEXT_PROCESSOR に
    # 'django.core.context_processors.request' が指定されていないと存在しない
    # ここでは敢えて存在しない場合にエラーを出すため直接参照している
    request = context['request']
    if lookup == 'published':
        qs = Announcement.objects.published(request.user)
    elif lookup == 'draft':
        qs = Announcement.objects.draft(request.user)
    return qs


@register.assignment_tag(takes_context=True)
def get_recent_announcements(context, lookup='published'):
    """
    get_announcementsで得られるQSのうち、作成日が1週間以内の物のみに絞り込む
    """
    qs = get_announcements(context, lookup)
    ct = timezone.now()
    seven_days_ago = ct - timezone.timedelta(days=7)
    return qs.filter(created_at__gte=seven_days_ago)
