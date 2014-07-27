# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/27
#
__author__ = 'giginet'

from haystack.forms import SearchForm

class KawazSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()