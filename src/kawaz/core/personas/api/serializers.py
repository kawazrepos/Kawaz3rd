from rest_framework import serializers
from ..models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    small_avatar = serializers.CharField(source='get_small_avatar', read_only=True)
    middle_avatar = serializers.CharField(source='get_middle_avatar', read_only=True)
    large_avatar = serializers.CharField(source='get_large_avatar', read_only=True)
    huge_avatar = serializers.CharField(source='get_huge_avatar', read_only=True)

    class Meta:
        model = Persona
        fields = (
            'id', 'nickname', 'quotes',
            'small_avatar', 'middle_avatar', 'large_avatar', 'huge_avatar',
            'gender', 'role',
        )
