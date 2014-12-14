from rest_framework import serializers
from kawaz.core.personas.models import Persona
from ..models import Material
from kawaz.core.personas.api.serializers import PersonaSerializer


class MaterialSerializer(serializers.ModelSerializer):
    author = PersonaSerializer(required=False, read_only=True)
    tag = serializers.CharField(source='get_attachment_tag', read_only=True)

    class Meta:
        model = Material
        fields = (
            'content_file', 'author', 'slug', 'ip_address', 'tag'
        )

    def create(self, validated_data):
        # django-rest-framework 3.0.1から明示的に書かなきゃいけなくなった
        # http://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        author_data = validated_data.pop('author')
        validated_data['author'] = Persona.objects.get(pk=author_data.pk)
        material = Material.objects.create(**validated_data)
        return material