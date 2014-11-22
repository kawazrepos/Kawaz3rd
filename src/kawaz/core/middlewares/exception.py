# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/935/
#
import sys
from django.views.debug import technical_500_response


class UserBasedExceptionMiddleware(object):
    """
    スーパーユーザーでアクセスしていた場合のみエラー時に詳細なエラーレポートを
    表示するためのミドルウェア
    """
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
