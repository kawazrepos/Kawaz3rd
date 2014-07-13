from django.utils.translation import ugettext as _
import django_filters
from django_filters import filters
from django_filters import widgets
from .models import Product
from .models import Category, Platform


class ProductFilter(django_filters.FilterSet):
    platforms = filters.ModelChoiceFilter(
        label=_('Platforms'),
        queryset=Platform.objects.all(),
        widget=widgets.LinkWidget(choices=[('', _('All'))]))

    categories = filters.ModelChoiceFilter(
        label=_('Categories'),
        queryset=Category.objects.all(),
        widget=widgets.LinkWidget(choices=[('', _('All'))]))

    class Meta:
        model = Product
        fields = ['platforms', 'categories',]
