# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from kawaz.api.views import KawazModelViewSet
from .serializers import StarSerializer
from ..models import Star


class StarViewSet(KawazModelViewSet):
    model = Star
    serializer_class = StarSerializer
    author_field_name = 'author'
