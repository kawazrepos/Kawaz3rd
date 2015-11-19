from .serializers import MaterialSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from kawaz.api import mixins
from kawaz.api.views import KawazGenericViewSet
from ..models import Material


class MaterialViewSet(mixins.CreateModelMixin,
                      KawazGenericViewSet):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    author_field_name = 'author'
    parser_classes = (FormParser, MultiPartParser, )

    def get_extra_fields(self):
        extras = super().get_extra_fields()
        ip_address = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
        extras.update({'ip_address': ip_address})
        return extras
