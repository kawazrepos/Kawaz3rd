# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/17
#
import datetime
from django.utils import timezone
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase
from kawaz.apps.events.tests.factories import EventFactory

__author__ = 'giginet'

class EventActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = EventFactory

    def test_create(self):
        """
        イベント作成時にActivityが生成される
        """
        self._test_create()

    def test_update_event(self):
        """
        以下のカラムを更新したとき、`_updated`フラグがコンテキストに入る
        """
        period_start = self.object.period_start + datetime.timedelta(hours=2)
        period_end = self.object.period_start + datetime.timedelta(hours=10)
        deadline = timezone.now() + datetime.timedelta(minutes=30)
        self._test_partial_update(
            (
                'period_start_updated',
                'period_end_updated',
                'place_updated',
            ),
            period_start=period_start,
            period_end=period_end,
            place='ジオフロント',
            number_restriction=10,
            attendance_deadline=deadline
        )

    def test_delete(self):
        """
        イベント削除時にActivityが生成される
        """
        self._test_delete()
