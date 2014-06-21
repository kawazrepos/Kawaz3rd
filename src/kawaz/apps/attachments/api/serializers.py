from rest_framework import serializers
from ..models import Material
from kawaz.core.personas.api.serializers import PersonaSerializer


class MaterialSerializer(serializers.ModelSerializer):
    author = PersonaSerializer(required=False, read_only=True)

    class Meta:
        model = Material
        fields = (
            'content_file', 'author', 'slug', 'ip_address'
        )
