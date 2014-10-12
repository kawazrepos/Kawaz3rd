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
def get_stars(context, object):
    """
    任意の<object>についた Star のクエリを取得し指定された
    <variable>に格納するテンプレートタグ
    ただし、ログイン中のユーザーが見れるスターのみが返却される

    Syntax:
        {% get_stars <object> as <variable> %}

    Examples:
        公開された Star のクエリを取得し、最新5件のみを描画

        {% get_stars object as stars %}
        {% for star in stars|slice:":5" %}
            {{ star }}
        {% endfor %}

    """
    request = context['request']
    qs = Star.objects.published(request.user).get_for_object(object)
    return qs
