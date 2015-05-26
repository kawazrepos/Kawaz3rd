from kawaz.api import mixins
from kawaz.api.views import KawazGenericViewSet
from .serializers import PersonaSerializer
from ..models import Persona
__author__ = 'giginet'


class PersonaViewSet(mixins.ListModelMixin,
                     KawazGenericViewSet):
    model = Persona
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
