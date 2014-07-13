#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/2
#
__author__ = 'giginet'

class SingleObjectPreviewMixin(object):
    """
    プレビュー用のビューを作るためのMixinです
    モデルインスタンスの代わりに辞書をcontextに渡して
    detailページをPreviewさせるために使います
    """

    def get_object(self, queryset=None):
        """
        get parameterで渡ってきた値からオブジェクトを作ります
        """
        fields = self.model._meta.fields
        params = self.request.GET.dict()
        obj = {k: v for k, v in params.items() if k in fields}
        return obj
