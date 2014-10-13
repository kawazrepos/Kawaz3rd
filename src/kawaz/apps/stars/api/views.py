from kawaz.api import mixins
from kawaz.api.views import KawazGenericViewSet
from .serializers import StarSerializer
from ..models import Star


class StarViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  KawazGenericViewSet):
    model = Star
    queryset = Star.objects.all().prefetch_related('author')
    serializer_class = StarSerializer
    author_field_name = 'author'
    filter_fields = ('content_type', 'object_id',)
