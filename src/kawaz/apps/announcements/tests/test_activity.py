from .factories import AnnouncementFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class EntryActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = AnnouncementFactory

    def test_create(self):
        self._test_create()

    def test_update(self):
        self._test_partial_update(body='本文変えました')

    def test_delete(self):
        self._test_delete()

    def test_comment_added(self):
        self._test_comment_added()
