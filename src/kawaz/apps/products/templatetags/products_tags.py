from django import template
from django.template import TemplateSyntaxError, Context
from django.template.loader import render_to_string
from django.conf import settings
from ..models import Product, URLRelease
from ..models import Platform
from ..models import Category

register = template.Library()


@register.assignment_tag
def get_products(lookup='mixed'):
    """
    任意の<lookup>によりフィルタされた Product のクエリを取得し指定された
    <variable>に格納するテンプレートタグ

    Syntax:
        {% get_products as <variable> %}
        {% get_products <lookup> as <variable> %}

    Lookup: (Default: mixed)
        mixed: display_mode が featured/tiled な Product を返す
        normal: display_mode が normal な Product を返す
        featured: display_mode が featured な Product を返す
        tiled: display_mode が tiled な Product を返す

    Examples:
        display_mode が featured/tiled な Product のクエリを取得し、最新
        5件のみを描画

        {% get_products as products %}
        {% for product in products|slice:":5" %}
            {{ product }}
        {% endfor %}

        display_mode が normal な Product を取得

        {% get_products 'normal' as normal_products %}
    """
    ALLOWED_LOOKUPS = ('mixed', 'normal', 'featured', 'tiled')
    if lookup not in ALLOWED_LOOKUPS:
        raise TemplateSyntaxError(
            "Unknown 'lookup' is specified to 'get_products'. "
            "It need to be one of {}.".format(ALLOWED_LOOKUPS))
    if lookup == 'mixed':
        qs = Product.objects.filter(display_mode__in=('featured', 'tiled'))
    else:
        qs = Product.objects.filter(display_mode__exact=lookup)
    return qs


@register.assignment_tag
def get_products_by_categories(categories):
    """
    任意のカテゴリに所属するProductを返却します

    categories:
        CategoryのQuerySet

    Example:
        {% load products_tag %}
        {% get_product_by_category <categories> as <variable> %}

    """
    qs = Product.objects.filter(categories__in=categories.all())
    return qs.distinct()


@register.assignment_tag
def get_relative(product):
    """
    任意のプロダクトの関連プロダクトを取り出します。
    渡されたプロダクトと同じカテゴリに所属している物全てから、自身を抜いた
    QuerySetを返します

    Syntax:
        {% get_relative <product> as <variable> %}
    """
    qs = Product.objects.filter(categories__in=product.categories.all())
    return qs.exclude(pk=product.pk).distinct()


@register.assignment_tag
def get_platforms():
    """
    全てのPlatform一覧を取り出します。

    Syntax:
        {% get_platforms as <variable> %}
    """
    qs = Platform.objects.all()
    return qs


@register.assignment_tag
def get_categories():
    """
    全てのCategory一覧を取り出します。

    Syntax:
        {% get_categories as <variable> %}
    """
    qs = Category.objects.all()
    return qs

@register.simple_tag(takes_context=True)
def render_twitter_card(context, product):
    """
    プロダクト用のTwitterカードを埋め込むテンプレートタグ
    通常はhead内に書く

    Syntax:
        {% render_twitter_card product %}

    Template:
        products/components/twitter_card.htmlが使用される。
        このテンプレートは以下のコンテキストを受け取れる

        product: 描画対象のProductオブジェクト
        apps: Productの所属するURLReleaseのうち、iOSアプリ、Androidアプリのもののみが含まれたリスト

        このような仕様になっているのは、appsがある場合のみTwitterカードのApp Cardを利用することが想定されているためである

    """
    request = context.get('request')
    url_releases = URLRelease.objects.filter(product=product)
    apps = [release for release in url_releases if release.is_appstore or release.is_googleplay]
    c = Context({
        'product': product,
        'apps': apps,
        'MEDIA_URL': settings.MEDIA_URL,
        'request': request
    })
    rendered = render_to_string("products/components/twitter_card.html", c)
    return rendered
