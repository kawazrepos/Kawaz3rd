# TODO: StarはAPIで提供する予定なので恐らくこのテンプレートタグは不要
#       完成時に本当に不要だった場合はメンテナンスのコスト削減のため
#       コード自体を削除する
from django import template
from django.template import TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType
from ..models import Star

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_star_endpoint(context, object):
    """
    任意の<object>に対するStarのエンドポイントURLを取得し、指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_star_endpoint <object> as <variable> %}

    Examples:
        あるオブジェクトに対するendpointを取得し、フォームを生成する

        {% get_star_endpoint object as endpoint %}
        <form action="{{ endpoint }}" method="POST">
            <input type="submit">
        </form>
    """
    from django.core.urlresolvers import reverse
    ct = ContentType.objects.get_for_model(object)
    # dataをdictで渡してしまうと、urllib.parse.urlencodeの
    # 並び順が保証されず毎回変わってしまう
    # そのため、あえてtupleで渡している
    data = (
        ('content_type', ct.pk),
        ('object_id', object.pk)
    )
    import urllib
    query = urllib.parse.urlencode(data)
    return '{}?{}'.format(reverse('star-list'), query)

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
        {% for star in stars|slice:":5" %}
            {{ star }}
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
