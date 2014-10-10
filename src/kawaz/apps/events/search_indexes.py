# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/27
#
__author__ = 'giginet'

from haystack import indexes
from django.utils import timezone
from .models import Event

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr='body')
    created_at = indexes.DateTimeField(model_attr='created_at')
    updated_at = indexes.DateTimeField(model_attr='updated_at')

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
