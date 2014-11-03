from django import template
from django.template import TemplateSyntaxError
from ..models import Entry, Category

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_entries(context, lookup='published'):
    """
    任意の<lookup>によりフィルタされた Entry のクエリを取得し指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_entries as <variable> %}
        {% get_entries <lookup> as <variable> %}

    Lookup: (Default: published)
        published: ユーザーに対して公開された Entry を返す
        draft: ユーザーが編集可能な下書き Entry を返す

    Examples:
        公開された Entry のクエリを取得し、最新5件のみを描画

        {% get_entries as entries %}
        {% for entry in entries|slice:":5" %}
            {{ entry }}
        {% endfor %}

        下書き記事を取得

        {% get_entries 'draft' as draft_entries %}
    """
    ALLOWED_LOOKUPS = ('published', 'draft')
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_entries'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    # 'request' は settings.TEMPLATE_CONTEXT_PROCESSOR に
    # 'django.core.context_processors.request' が指定されていないと存在しない
    # ここでは敢えて存在しない場合にエラーを出すため直接参照している
    request = context['request']
    if lookup == 'published':
        qs = Entry.objects.published(request.user)
    elif lookup == 'draft':
        qs = Entry.objects.draft(request.user)
    return qs

@register.assignment_tag(takes_context=True)
def get_published_entries_of(context, author):
    """
    あるユーザーの書いたpublishedなエントリーを返します

    Syntax:
        {% get_published_entries_of <user> as <variable> %}
    """
    qs = get_entries(context)
    return qs.filter(author=author)

@register.assignment_tag
def get_categories(author=None):
    """
     ブログ記事カテゴリ一覧を取り出します
     <user>を渡した場合は、そのユーザーが持っているカテゴリのみを取り出します

     Syntax:
        {% get_categories as categories %}
        {% get_categories <user> as categories %}
    """
    qs = Category.objects.all()
    if author:
        qs = qs.filter(author__pk=author.pk)
    return qs

@register.assignment_tag(takes_context=True)
def get_hotentries(context, author=None):
    """
    ホッテントリの一覧を取り出します
    <user>を渡した場合は、そのユーザーが作成した物のみに絞り込まれます

    Syntax:
        {% get_hotentries as entries %}
        {% get_hotentries <user> as entries %}
    """
    user = getattr(context['request'], 'user', None)
    qs = Entry.objects.published(user).get_hotentries()
    if author:
        qs = qs.filter(author__pk=author.pk)
    return qs
