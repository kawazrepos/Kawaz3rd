# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/19
#
__author__ = 'giginet'
from rest_framework import serializers
from kawaz.core.personas.api.serializers import PersonaSerializer
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    ブログカテゴリ用のAPIシリアライザ
    """
    author = PersonaSerializer(required=False,
                               read_only=True,
                               default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = (
            'id', 'author', 'label'
        )
