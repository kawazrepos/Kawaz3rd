from kawaz.api.views import KawazModelViewSet
from .serializers import StarSerializer
from ..models import Star
from rest_framework import mixins
from rest_framework.response import Response

class StarViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  KawazModelViewSet):
    model = Star
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    author_field_name = 'author'
    filter_fields = ('content_type', 'object_id',)
