from rest_framework import serializers
from django.template.loader import render_to_string
from kawaz.core.personas.api.serializers import PersonaSerializer
from ..models import Star


class StarSerializer(serializers.ModelSerializer):
    author = PersonaSerializer(required=False, read_only=True)
    content_type = serializers.PrimaryKeyRelatedField()
    html = serializers.SerializerMethodField('get_html')
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
