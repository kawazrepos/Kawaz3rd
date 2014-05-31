from rest_framework import serializers
from ..models import Material


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = (
            'content_file', 'author', 'slug', 'id_address', 'create_at'
        )