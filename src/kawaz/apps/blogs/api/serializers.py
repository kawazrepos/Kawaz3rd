# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/19
#
from kawaz.core.personas.models import Persona


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

    def create(self, validated_data):
        # django-rest-framework 3.0.1から明示的に書かなきゃいけなくなった
        # http://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        author_data = validated_data.pop('author')
        validated_data['author'] = Persona.objects.get(pk=author_data.pk)
        category = Category.objects.create(**validated_data)
        return category
