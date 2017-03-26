import random
import string
import datetime
from itertools import chain
from django.test import TestCase
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import get_default_timezone
from ..factories import PersonaFactory, AccountFactory
from ..factories import ProfileFactory
from ..factories import ServiceFactory
from ...models import Profile
from ...models import Account


BASE_URL = 'members/my/profile'


def random_str(n=10):
    return ''.join(
        [random.choice(string.ascii_letters + string.digits)
         for i in range(n)]
    )


class ProfileViewTestCaseBase(TestCase):

    def setUp(self):
        self.members = (
                ProfileFactory(user__role='adam').user,
                ProfileFactory(user__role='seele').user,
                ProfileFactory(user__role='nerv').user,
                ProfileFactory(user__role='children').user,
            )
        self.non_members = (
                PersonaFactory(role='wille'),
            )
        self.anonymous = AnonymousUser()
        self.services = (
            ServiceFactory(),
            ServiceFactory(label='Facebook')
        )

    def prefer_login(self, user):
        if user.is_authenticated():
            # user としてアクセスするためにログイン
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))


class ProfileUpdateViewTestCase(ProfileViewTestCaseBase):

    def setUp(self):
        super().setUp()
        self.profile_kwargs = {
            'pub_state' : 'public',
            'place' : '札幌市北区',
            'url' : 'http://www.kawaz.org/members/kawaztan/',
            'remarks' : 'けろーん',
            'birth_day' : datetime.datetime.today(),
            'accounts-TOTAL_FORMS': 0,  # アカウントは作成しない
            'accounts-INITIAL_FORMS': 1,
            'accounts-MAX_NUM_FORMS': 1000,
        }

    def test_reverse_persona_detail_url(self):
        """
        ProfileUpdateViewの逆引き
        """
        self.assertEqual(
            reverse('personas_profile_update'),
            '/{}/update/'.format(BASE_URL),
        )

    def test_non_members_cannot_access_profile_update_view(self):
        """
        メンバー以外プロフィール編集ページにアクセスした場合は404
        """
        url = reverse('personas_profile_update')
        for user in chain(self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertEqual(r.status_code, 404)

    def test_members_can_access_profile_update_view(self):
        """
        メンバーはユーザー編集ページにアクセス可能
        """
        url = reverse('personas_profile_update')
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'personas/profile_form.html')
            self.assertTrue('object' in r.context_data)
            self.assertEqual(r.context_data['object'],
                             user._profile)
            # アカウント用フォームセットが含まれているか？
            self.assertTrue('formset' in r.context)

    def test_non_members_cannot_update_profile(self):
        """
        非メンバーはプロフィール情報を編集できない
        """
        url = reverse('personas_profile_update')
        for user in chain(self.non_members, [self.anonymous]):
            self.prefer_login(user)
            r = self.client.post(url, self.profile_kwargs)
            self.assertEqual(r.status_code, 404)

    def test_members_can_update_own_profile(self):
        """
        メンバーは自身のプロフィール情報を編集できる
        """
        url = reverse('personas_profile_update')
        for user in self.members:
            self.prefer_login(user)
            r = self.client.post(url, self.profile_kwargs)
            self.assertRedirects(r, user.get_absolute_url())
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 編集されているかチェック
            p = Profile.objects.get(user=user)
            self.assertEqual(p.place, '札幌市北区')

    def test_members_can_assign_multiple_accounts(self):
        """
        メンバーは自身のプロフィールに対し複数のアカウントを設定可能
        """
        kwargs = dict(self.profile_kwargs)
        url = reverse('personas_profile_update')
        for i, user in enumerate(self.members):
            username1 = "{}-{}".format(random_str(), i)
            username2 = "{}-{}".format(random_str(), i)
            kwargs.update({
                'accounts-0-service': self.services[0].pk,
                'accounts-0-username': username1,
                'accounts-0-pub_state': 'public',
                'accounts-1-service': self.services[1].pk,
                'accounts-1-username': username2,
                'accounts-1-pub_state': 'public',
                'accounts-TOTAL_FORMS': 2,
                'accounts-INITIAL_FORMS': 0,
                'accounts-MAX_NUM_FORMS': 1000,
            })
            self.prefer_login(user)
            r = self.client.post(url, kwargs)
            self.assertRedirects(r, user.get_absolute_url())
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 編集されているかチェック
            p = Profile.objects.get(user=user)
            a = Account.objects.filter(profile=p)
            self.assertEqual(a.count(), 2)
            self.assertEqual(a[0].service.pk, self.services[0].pk)
            self.assertEqual(a[0].profile.user, user)
            self.assertEqual(a[0].username, username1)
            self.assertEqual(a[0].pub_state, 'public')
            self.assertEqual(a[1].profile.user, user)
            self.assertEqual(a[1].service.pk, self.services[1].pk)
            self.assertEqual(a[1].username, username2)
            self.assertEqual(a[1].pub_state, 'public')

    def test_members_can_delete_account(self):
        """
        メンバーは自身のプロフィールに既に登録されているアカウントを削除可能
        """
        kwargs = dict(self.profile_kwargs)
        url = reverse('personas_profile_update')

        for i, user in enumerate(self.members):
            # 予めアカウントを作成しておく
            p = Profile.objects.get(user=user)
            account = AccountFactory(profile=p)
            a = Account.objects.filter(profile=p)
            self.assertEqual(a.count(), 1)
            self.assertIn(account, a)

            # アカウントを削除する
            kwargs.update({
                'accounts-0-id': account.pk,
                'accounts-0-service': account.service,
                'accounts-0-username': account.username,
                'accounts-0-pub_state': account.pub_state,
                'accounts-0-profile': p.pk,
                'accounts-0-DELETE': True,
                'accounts-TOTAL_FORMS': 1,
                'accounts-INITIAL_FORMS': 1,
                'accounts-MAX_NUM_FORMS': 1000,
            })
            self.prefer_login(user)
            r = self.client.post(url, kwargs)
            self.assertRedirects(r, user.get_absolute_url())
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")

            # アカウントが削除されているかチェックする
            p = Profile.objects.get(user=user)
            a = Account.objects.filter(profile=p)
            self.assertEqual(a.count(), 0)
            self.assertNotIn(account, a)


class ProfilePreviewViewTestCase(ProfileViewTestCaseBase):

    def test_anybody_can_access_profile_preview_view(self):
        """
        だれでもプロフィールプレビューページにアクセス可能

        Note:
            プロフィールプレビューページはGETのパラメータで渡された値から
            仮想オブジェクトを作成して描画するビューなので閲覧制限を行う
            必要がない
        """
        url = reverse('personas_profile_preview')
        for user in chain(self.members, self.non_members, [self.anonymous]):
            self.prefer_login(user)
            import json
            r = self.client.post(url, json.dumps({}), content_type='application/json')
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'personas/profile_preview.html')
            self.assertTrue('object' in r.context_data)

class ServiceDetailViewTestCase(TestCase):

    def test_can_access(self):
        service = ServiceFactory()
        r = self.client.get(service.get_absolute_url())
        self.assertTemplateUsed(r, 'personas/service_detail.html')

        self.assertIn('all_services', r.context)
        self.assertIn(service, r.context['all_services'])
