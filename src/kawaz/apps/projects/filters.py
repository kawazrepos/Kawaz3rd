from django.utils.translation import ugettext as _
import django_filters
from django_filters import filters
from django_filters import widgets
from .models import Project


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = ()
        order_by = ['title', 'category', 'status', 'created_at',]
