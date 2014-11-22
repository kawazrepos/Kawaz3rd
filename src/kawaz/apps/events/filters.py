# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/9/28
#
__author__ = 'giginet'
from django.utils.translation import ugettext_lazy as _
import django_filters
from django_filters import filters
from .models import Event
from .models import Category
from kawaz.core.filters.widgets import ListGroupLinkWidget


class EventFilter(django_filters.FilterSet):
    category = filters.ModelChoiceFilter(
        label=_('Categories'),
        queryset=Category.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))]))

    class Meta:
        model = Event
        fields = ['category',]
