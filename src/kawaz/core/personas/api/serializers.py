from rest_framework import serializers
from ..models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = Persona
        fields = (
            'id', 'nickname', 'quotes',
            'avatar', 'gender', 'role',
        )
