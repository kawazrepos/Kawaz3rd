# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from rest_framework import serializers
from ..models import Star


class StarSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    content_type = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Star
        fields = (
            'id', 'content_type', 'object_id',
            'author', 'quote',
        )
