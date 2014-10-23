# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from kawaz.apps.products.tests.factories import ProductFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class ProductActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = ProductFactory

    def test_create(self):
        self._test_create()

    def test_update(self):
        self._test_partial_update(description='本文変えました')

    def test_delete(self):
        self._test_delete()

    def test_add_comment(self):
        self._test_add_comment()
