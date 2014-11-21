# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from kawaz.apps.blogs.tests.factories import EntryFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class EntryActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = EntryFactory

    def test_create(self):
        self._test_create()

    def test_update(self):
        self._test_partial_update(context_names=('title_updated', 'body_updated'), title="タイトル変えました", body='本文変えました')

    def test_delete(self):
        self._test_delete()

    def test_comment_added(self):
        self._test_comment_added()
