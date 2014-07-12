import django_filters
from .models import Product

__author__ = 'giginet'

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['platforms', 'categories',]
