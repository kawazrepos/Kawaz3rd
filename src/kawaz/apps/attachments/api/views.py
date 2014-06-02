from kawaz.api.views import KawazGenericViewSetMixin
from django.shortcuts import get_object_or_404
from .serializers import MaterialSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from ..models import Material

class MaterialViewSetMixin(KawazGenericViewSetMixin, mixins.CreateModelMixin,
                           GenericViewSet):
    lookup_field = 'slug'
    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    author_field_name = 'author'
    parser_classes = (FileUploadParser,)

    def pre_save(self, obj):
        super().pre_save(obj)
        obj.ip_address = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
