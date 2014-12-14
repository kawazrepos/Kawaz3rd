from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.template.loader import render_to_string
from kawaz.core.personas.api.serializers import PersonaSerializer
from kawaz.core.personas.models import Persona
from ..models import Star


class StarSerializer(serializers.ModelSerializer):
    author = PersonaSerializer(required=False)
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    html = serializers.SerializerMethodField()
    tooltip = serializers.CharField(source='tooltip_text', read_only=True)

    def get_html(self, obj):
        # スターの描画用テンプレートを返す
        return render_to_string('components/star.html', {
            'star': obj,
            'from_api': True
        })

    class Meta:
        model = Star
        fields = (
            'id', 'content_type', 'object_id',
            'author', 'quote', 'html', 'tooltip'
        )

    def create(self, validated_data):
        # django-rest-framework 3.0.1から明示的に書かなきゃいけなくなった
        # http://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        author_data = validated_data.pop('author')
        validated_data['author'] = Persona.objects.get(pk=author_data.pk)
        star = Star.objects.create(**validated_data)
        return star
