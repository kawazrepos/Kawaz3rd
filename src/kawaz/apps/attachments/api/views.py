from kawaz.api.views import KawazModelViewSet
from django.shortcuts import get_object_or_404
from .serializers import MaterialSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework import mixins
from ..models import Material

class MaterialViewSet(KawazModelViewSet,
                      mixins.CreateModelMixin):
    lookup_field = 'slug'
    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    author_field_name = 'author'
    parser_classes = (FileUploadParser,)

    def pre_save(self, obj):
        super().pre_save(obj)
        try:
            obj.ip_address = self.request.META['REMOTE_ADDR']
        except:
            obj.ip_address = '0.0.0.0'
