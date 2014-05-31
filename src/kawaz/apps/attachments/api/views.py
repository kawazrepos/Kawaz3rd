from kawaz.api.views import KawazModelViewSet
from django.shortcuts import get_object_or_404
from .serializers import MaterialSerializer
from ..models import Material
from rest_framework.response import Response

class MaterialViewSet(KawazModelViewSet):
    model = Material
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    author_field_name = 'author'
