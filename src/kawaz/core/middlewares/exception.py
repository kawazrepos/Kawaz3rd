# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/935/
#
import sys
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.views.debug import technical_500_response


class UserBasedExceptionMiddleware(object):
    """
    スーパーユーザーでアクセスしていた場合のみエラー時に詳細なエラーレポートを
    表示するためのミドルウェア
    """
    def __init__(self):
        if settings.DEBUG or settings.TESTING:
            # デバッグモードもしくはテスト中はこのミドルウェアを無効化
            raise MiddlewareNotUsed

    def process_exception(self, request, exception):
        """
        スーパーユーザーの場合は例外に対して詳細なレポートを表示
        """
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
