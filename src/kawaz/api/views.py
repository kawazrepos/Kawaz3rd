from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import filters
from .filters import KawazObjectPermissionFilterBackend
from . import mixins


class KawazGenericViewSet(GenericViewSet):
    renderer_classes = (JSONRenderer,)
    author_field_name = None
    permission_classes = (DjangoObjectPermissions, DjangoModelPermissions)
    filter_backends = (
        filters.DjangoFilterBackend,
        KawazObjectPermissionFilterBackend
    )


class KawazReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                KawazGenericViewSet):
    """
    パーミッションを考慮した読み込み専用のViewSetです
    retrieve, list のみを提供します
    """


class KawazModelViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        KawazGenericViewSet):
    """
    パーミッションを考慮した汎用的なViewSetです
    retrieve, listに加え、create, destroy, update, partial_updateを提供します
    """
    def pre_save(self, obj):
        if obj.pk is None:
            # newly created
            mixins.CreateModelMixin.pre_save(self, obj)
        else:
            mixins.UpdateModelMixin.pre_save(self, obj)
