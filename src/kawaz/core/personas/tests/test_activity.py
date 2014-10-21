# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from .factories import PersonaFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class PersonaActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = PersonaFactory

    def test_update(self):
        self._test_partial_update(nickname='ニックネーム変えました')
