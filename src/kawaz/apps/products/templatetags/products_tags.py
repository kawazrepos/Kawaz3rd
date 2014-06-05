from django import template
from django.template import TemplateSyntaxError
from ..models import Product

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
