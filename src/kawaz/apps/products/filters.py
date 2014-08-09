from django.utils.translation import ugettext as _
import django_filters
from django_filters import filters
from .models import Product
from .models import Category, Platform
from kawaz.core.filters.widgets import ListGroupLinkWidget


class ProductFilter(django_filters.FilterSet):
    platforms = filters.ModelChoiceFilter(
        label=_('Platforms'),
        queryset=Platform.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))]))

    categories = filters.ModelChoiceFilter(
        label=_('Categories'),
        queryset=Category.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))]))

    class Meta:
        model = Product
        fields = ['platforms', 'categories',]
