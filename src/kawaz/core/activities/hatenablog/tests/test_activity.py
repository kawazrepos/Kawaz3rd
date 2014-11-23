from kawaz.core.activities.hatenablog.tests.factories import HatenablogEntryFactory

__author__ = 'giginet'
import datetime
from django.template import Context
from activities.models import Activity
from activities.registry import registry
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class HatenaBlogEntryActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = HatenablogEntryFactory

    def test_create(self):
        """
        広報ブログ記事の作成イベントは通知される
        """
        self._test_create()

    def test_update(self):
        """
        広報ブログ記事の更新イベントは通知されない
        """
        entry = HatenablogEntryFactory()
        nactivity = Activity.objects.count()
        entry.title = "hogehoge"
        entry.save()
        self.assertEqual(Activity.objects.count(), nactivity)

    def test_delete(self):
        """
        広報ブログ記事の削除イベントは通知されない
        """
        entry = HatenablogEntryFactory()
        nactivity = Activity.objects.count()
        entry.delete()
        self.assertEqual(Activity.objects.count(), nactivity)
