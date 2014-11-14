import json

class SingleObjectPreviewMixin(object):

    """
    プレビューを行うためのViewを作るMixin

    SingleObjectMixin と共に使用することが前提で、SingleObjectMixin にて定義
    される `get_object(queryset=None)` メソッドを上書きする。
    上記上書きされたメソッドは POST にて渡されたパラメータを元に仮想モデル
    インスタンスを生成し返すため、このMixinが適用されたビューはモデルの保存
    などを行わずしてテンプレートにてモデルインスタンスのように扱うことが可能

    Note:
        実際に返されるオブジェクトは辞書であるためテンプレート以外では動かない

        RESTの原則的にはGETで行うのがふさわしいが、GETだと、長い本文を送信したときに
        413エラーを送出してしまうため、POSTで行っている
    """

    def get_object(self, queryset=None):
        """
        POSTで渡された値を元に仮想オブジェクトを構築し返す
        """
        # Use 'queryset' of specified or 'get_queryset'
        queryset = queryset or self.get_queryset()
        # Use 'model' of queryset or 'model' attribute
        model = getattr(queryset, 'model', self.model)
        fields = model._meta.get_all_field_names()
        # Ref https://docs.djangoproject.com/en/dev/releases/1.5/#non-form-data-in-http-requests
        # http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
        # Django1.5からAjaxではrequest.POSTでQueryDictを取れなくなったので、JSONに変換している
        params = json.loads(self.request.body.decode('utf-8'))
        # filter field values
        return {k: v for k, v in params.items() if k in fields}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)