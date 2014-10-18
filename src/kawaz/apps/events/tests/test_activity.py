# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/17
#
from kawaz.apps.activities.tests.testcases import BaseActivityMediatorTestCase
from kawaz.apps.events.tests.factories import EventFactory

__author__ = 'giginet'



class EventActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = EventFactory

    def test_create(self):
        self._test_create()

    def test_update_event(self):
        """
        場所を更新したとき、`place_updated`フラグがコンテキストに入る
        """
        self._test_partial_update(
            {'place': 'ジオフロント'},
            ('place_updated',)
        )

