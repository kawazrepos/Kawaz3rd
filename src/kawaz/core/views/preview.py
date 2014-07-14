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
        params = self.request.GET.dict()
        return params
