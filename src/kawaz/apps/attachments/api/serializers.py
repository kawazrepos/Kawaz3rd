from rest_framework import serializers
from ..models import Material


class MaterialSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Material
        fields = (
            'content_file', 'author', 'slug', 'ip_address'
        )