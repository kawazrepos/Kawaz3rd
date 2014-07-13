from django.utils.translation import ugettext as _

import django_filters
from django_filters import filters
from django_filters import widgets

from .models import Product
from .models import Category, Platform

__author__ = 'giginet'

class ProductFilter(django_filters.FilterSet):

    def _choices_with_deselect(qs):
        """
        ModelChoiceFilterを利用すると、全ての指定ができなくなってしまう
        そのため、このようにchoicesをquerysetから生成してChoiceFilterに渡している
        """
        choices = [(query.pk, str(query)) for query in qs]
        return [('', _('Any')),] + choices

    platforms = filters.ChoiceFilter(choices=_choices_with_deselect(Platform.objects.all()), widget=widgets.LinkWidget())
    categories = filters.ChoiceFilter(choices=_choices_with_deselect(Category.objects.all()), widget=widgets.LinkWidget())

    class Meta:
        model = Product
        fields = ['platforms', 'categories',]
