from rest_framework import serializers
from kawaz.core.personas.api.serializers import PersonaSerializer
from ..models import Star


class StarSerializer(serializers.ModelSerializer):
    author = PersonaSerializer(required=False, read_only=True)
    content_type = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Star
        fields = (
            'id', 'content_type', 'object_id',
            'author', 'quote',
        )
