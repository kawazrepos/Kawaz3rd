import datetime
from django.template import Context
from activities.models import Activity
from activities.registry import registry
from ..models.profile import Profile
from .factories import PersonaFactory, ProfileFactory, AccountFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase


class PersonaActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = PersonaFactory

    def test_create(self):
        """
        Personaの作成イベントは通知されない
        """
        nactivity = Activity.objects.count()
        PersonaFactory()
        self.assertEqual(Activity.objects.count(), nactivity)

    def test_update(self):
        """
        Personaの更新イベントは通知されない
        """
        persona = PersonaFactory()
        nactivity = Activity.objects.count()
        persona.nickname = "new nickname"
        persona.save()
        self.assertEqual(Activity.objects.count(), nactivity)

    def test_delete(self):
        """
        Personaの削除イベントは通知されない
        """
        persona = PersonaFactory()
        nactivity = Activity.objects.count()
        persona.delete()
        self.assertEqual(Activity.objects.count(), nactivity)

    def test_comment_added(self):
        self._test_comment_added()

    def test_activated(self):
        """
        Profileが作成されたとき、activatedイベントが発行される
        """
        nactivity = Activity.objects.count()
        profile = ProfileFactory()
        self.assertEqual(Activity.objects.count(), nactivity + 1)
        activity = Activity.objects.first()
        self.assertEqual(activity.status, 'activated')
        self.assertEqual(activity.snapshot,
                         profile.user)

    def test_update_profile(self):
        """
        ユーザーのProfileを更新したとき、profile_updated Activityが発行される
        """
        profile = ProfileFactory()

        # Profileを更新する
        fields = {
            'place': 'ネルフ本部',
            'birthday': datetime.date(2112, 9, 21),
            'url': 'http://nerv.com/',
            'remarks': 'ねむい',
        }
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

    def test_delete(self):
        """
        Profileの削除イベントは通知されない
        """
        profile = ProfileFactory()
        nactivity = Activity.objects.count()
        profile.delete()
        self.assertEqual(Activity.objects.count(), nactivity)

    def test_account_added(self):
        """
        アカウントを作成したとき、ユーザーに対してaccount_added Activityが
        発行される
        """

        # アカウントを作る
        account = AccountFactory()

        # Personaに対して、profile_updatedが発行されている
        activities = Activity.objects.get_for_object(account.profile.user)
        self.assertEqual(len(activities), 2)
        activity = activities[0]
        self.assertEqual(activity.status, 'account_added')

        # activityのremarksにアカウントのpkが設定されている
        self.assertEqual(activity.remarks, str(account.pk))

        # contextにaccount, serviceを含んでいる
        mediator = registry.get(activity)
        context = Context()
        context = mediator.prepare_context(activity, context)
        self.assertEqual(context['account'], account)
        self.assertEqual(context['service'], account.service)

