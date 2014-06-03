from kawaz.api.views import KawazGenericViewSetMixin
from .serializers import StarSerializer
from ..models import Star
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

class StarViewSetMixin(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       KawazGenericViewSetMixin,
                       GenericViewSet):
    model = Star
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    author_field_name = 'author'
    filter_fields = ('content_type', 'object_id',)
