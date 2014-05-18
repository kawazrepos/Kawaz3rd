# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from tastypie.resources import ModelResource


class KawazModelResource(ModelResource):
    """
    Kawaz API 用のベースリソースクラス

    1.  `author_field_name` が指定されている場合、オブジェ作成時に自動的に
        そのフィールドにAPI使用ユーザを割り当て
    2.  `published` メソッドが対象モデルのマネージャに定義されている場合は
        API使用ユーザによりフィルタリングする

    """
    author_field_name = None

    def obj_create(self, bundle, **kwargs):
        user_obj = bundle.request.user
        if self.author_field_name and user_obj.is_authenticated():
            kwargs[self.author_field_name] = user_obj
        return super().obj_create(bundle, **kwargs)

    def get_object_list(self, request):
        model = self._meta.object_class
        user_obj = request.user
        if hasattr(model.objects, 'published'):
            # published によるフィルタリング
            qs = model.objects.published(user_obj)
            # UPDATE/DELETE などは下書き状態の物に対しても機能するべきなので
            # 自身が所有しているオブジェクトクエリも追加する
            if self.author_field_name and user_obj.is_authenticated():
                kwargs = {self.author_field_name: user_obj}
                qs |= model.objects.filter(**kwargs)
                # 重複が発生する可能性があるため取り除く
                qs = qs.distinct()
        else:
            qs = super().get_object_list(request)
        return qs
