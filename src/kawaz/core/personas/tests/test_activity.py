# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
import datetime
from django.template import Context
from activities.models import Activity
from activities.registry import registry
from .factories import PersonaFactory, ProfileFactory, AccountFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class PersonaActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = PersonaFactory

    def test_update(self):
        self._test_partial_update(('nickname_updated', 'gender_updated', 'avatar_created', 'is_active_deleted'),
                                  nickname='ニックネーム変えました',
                                  gender='man',
                                  avatar='icon.png',
                                  is_active=False)

    def test_add_comment(self):
        self._test_add_comment()

    def test_update_profile(self):
        """
        あるユーザーのProfileを更新したとき、profile_updated Activityが発行される
        """
        profile = ProfileFactory()

        # Profileを更新する
        fields = {'place': 'ネルフ本部', 'birthday': datetime.datetime(2112, 9, 21), 'url': 'http://nerv.com/', 'remarks': 'ねむい'}
        activities = Activity.objects.get_for_object(profile.user)
        self.assertEqual(len(activities), 1)
        for field, value in fields.items():
            setattr(profile, field, value)
        profile.save()

        # Personaに対して、profile_updatedが発行されている
        activities = Activity.objects.get_for_object(profile.user)
        self.assertEqual(len(activities), 2)
        activity = activities[0]
        self.assertEqual(activity.status, 'profile_updated')

        # contextにフラグを含んでいる
        mediator = registry.get(activity)
        context = Context()
        context = mediator.prepare_context(activity, context)
        self._test_render(activities[0])

        # contextにprofileを含んでいる
        self.assertEqual(context['profile'], profile)

    def test_add_account(self):
        """
        アカウントを作成したとき、ユーザーに対してadd_account Activityが発行される
        """

        # アカウントを作る
        account = AccountFactory()

        # Personaに対して、profile_updatedが発行されている
        activities = Activity.objects.get_for_object(account.profile.user)
        self.assertEqual(len(activities), 2)
        activity = activities[0]
        self.assertEqual(activity.status, 'add_account')

        # activityのremarksにアカウントのpkが設定されている
        self.assertEqual(activity.remarks, str(account.pk))

        # contextにaccount, serviceを含んでいる
        mediator = registry.get(activity)
        context = Context()
        context = mediator.prepare_context(activity, context)
        self.assertEqual(context['account'], account)
        self.assertEqual(context['service'], account.service)

