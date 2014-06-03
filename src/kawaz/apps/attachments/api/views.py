from .serializers import MaterialSerializer
from rest_framework.parsers import FileUploadParser
from kawaz.api import mixins
from kawaz.api.views import KawazGenericViewSet
from ..models import Material


class MaterialViewSetMixin(mixins.CreateModelMixin,
                           KawazGenericViewSet):
    lookup_field = 'slug'
    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    author_field_name = 'author'
    parser_classes = (FileUploadParser,)

    def pre_save(self, obj):
        super().pre_save(obj)
        obj.ip_address = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
