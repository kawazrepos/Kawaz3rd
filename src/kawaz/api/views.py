from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import filters
from .filters import KawazObjectPermissionFilterBackend
from . import mixins


class KawazGenericViewSet(GenericViewSet):
    """
    Kawaz で使用する API が通常行う設定を事前に行った GenericViewSet
    下記に上げる設定が行われている

    - レスポンスをデフォルトでJSONで返すように指定
    - 権限チェックに DjangoModelPermissions と DjangoObjectPermissions を指定
    - フィルターバックエンドに DjangoFilterBackend と
      KawazObjectPermissionFilterBackend を指定

    注意:
        KawazObjectPermissionFilterBackend は全てのオブジェクトの権限をループ
        で検索するバックエンドのため大量のオブジェクトに対して実行すると実働
        時間がかかる可能性が存在する
    """
    renderer_classes = (JSONRenderer,)
    permission_classes = (DjangoObjectPermissions, DjangoModelPermissions)
    filter_backends = (
        filters.DjangoFilterBackend,
        KawazObjectPermissionFilterBackend
    )


class KawazReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                KawazGenericViewSet):
    """
    KawazGenericViewSet をベースとした読み込み専用APIのViewSet
    retrieve, list のみを提供
    """


class KawazModelViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        KawazGenericViewSet):
    """
    KawazGenericViewSet をベースとした読み書き用APIのViewSet
    retrieve, list に加え create, destroy, update, partial_update を提供
    """
    def pre_save(self, obj):
        # 新規作成か否かにより自動的に呼び出す必要のあるMixinを決定し実行
        if obj.pk is None:
            mixins.CreateModelMixin.pre_save(self, obj)
        else:
            mixins.UpdateModelMixin.pre_save(self, obj)
