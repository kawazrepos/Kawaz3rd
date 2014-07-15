class SingleObjectPreviewMixin(object):

    """
    プレビューを行うためのViewを作るMixin

    SingleObjectMixin と共に使用することが前提で、SingleObjectMixin にて定義
    される `get_object(queryset=None)` メソッドを上書きする。
    上記上書きされたメソッドは GET にて渡されたパラメータを元に仮想モデル
    インスタンスを生成し返すため、このMixinが適用されたビューはモデルの保存
    などを行わずしてテンプレートにてモデルインスタンスのように扱うことが可能

    Note:
        実際に返されるオブジェクトは辞書であるためテンプレート以外では動かない
    """

    def get_object(self, queryset=None):
        """
        GETで渡された値を元に仮想オブジェクトを構築し返す
        """
        # Use 'queryset' of specified or 'get_queryset'
        queryset = queryset or self.get_queryset()
        # Use 'model' of queryset or 'model' attribute
        model = getattr(queryset, 'model', self.model)
        fields = model._meta.get_all_field_names()
        params = self.request.GET.dict()
        # filter field values
        return {k: v for k, v in params.items() if k in fields}
