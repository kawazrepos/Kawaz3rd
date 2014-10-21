# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from .factories import ProfileFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class ProfileActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = ProfileFactory

    def test_update(self):
        self._test_partial_update(place='本文変えました')
