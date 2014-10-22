# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
import datetime
from activities.models import Activity
from .factories import ProfileFactory, AccountFactory
from kawaz.apps.events.tests.factories import EventFactory
from kawaz.apps.profiles.models import Profile
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class ProfileActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = ProfileFactory

    def test_update(self):
        self._test_partial_update(('place_updated', 'birthday_updated', 'url_updated',),
            place='本文変えました',
            remarks="remarks",
            birthday=datetime.datetime(2112, 9, 21),
            url="http://www.kantei.go.jp/")

    def test_add_account(self):
        """
        アカウント追加時に通知される
        """
        nactivity = Activity.objects.get_for_model(Profile).count()

        account = AccountFactory(profile=self.object)
        self.assertEqual(nactivity+1,
                         Activity.objects.get_for_model(Profile).count())
        activity = Activity.objects.get_for_model(Profile).first()
        self.assertEqual(activity.snapshot, account)
        self.assertEqual(activity.status, 'account_add')
        self.assertTrue(str(account.pk) in activity.remarks)

        account2 = AccountFactory(profile=self.object, username="account2")
        self.assertEqual(nactivity+2,
                         Activity.objects.get_for_model(Profile).count())
        activity = Activity.objects.get_for_model(Profile).first()
        self.assertEqual(activity.snapshot, account2)
        self.assertEqual(activity.status, 'account_add')
        self.assertTrue(str(account2.pk) in activity.remarks)

    def test_remove_account(self):
        """
        アカウント削除時に通知される
        """
        account = AccountFactory(profile=self.object)
        account2 = AccountFactory(profile=self.object, username="account2")
        nactivity = Activity.objects.get_for_model(Profile).count()

        account_pk = account.pk
        account.delete()

        self.assertEqual(nactivity+1,
                         Activity.objects.get_for_model(Profile).count())
        activity = Activity.objects.get_for_model(Profile).first()
        self.assertEqual(activity.snapshot.pk, account_pk)
        self.assertEqual(activity.status, 'account_remove')
        self.assertEqual(activity.remarks, str(account_pk))

        account2_pk = account2.pk
        account2.delete()

        self.assertEqual(nactivity+2,
                         Activity.objects.get_for_model(Profile).count())
        activity = Activity.objects.get_for_model(Profile).first()
        self.assertEqual(activity.snapshot.pk, account2_pk)
        self.assertEqual(activity.status, 'account_remove')
        self.assertEqual(activity.remarks, str(account2_pk))