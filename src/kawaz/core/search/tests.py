# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/27
#
__author__ = 'giginet'

from django.test import TestCase

class SearchViewTestCase(TestCase):
    def test_search_view(self):
        """
        /search/で検索用のビューが見れるかどうか
        """
        r = self.client.get('/search/')
        self.assertTemplateUsed(r, 'search/search.html')