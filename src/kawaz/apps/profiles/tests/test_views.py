import datetime
from django.test import TestCase
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from .factories import ProfileFactory
from .factories import ServiceFactory
from ..models import Profile
from ..models import Account
from kawaz.core.personas.tests.factories import PersonaFactory
from django.utils.timezone import get_default_timezone


BASE_URL = 'profiles'


class ProfileUpdateViewTestCase(TestCase):

    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.other = PersonaFactory()
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.profile = ProfileFactory(user=self.user)

        self.services = (ServiceFactory(), ServiceFactory(label='Facebook'))

    def test_anonymous_user_can_not_view_profile_update_view(self):
        '''Tests anonymous user can not view ProfileUpdateView'''
        r = self.client.get('/{}/update/'.format(BASE_URL))
        self.assertRedirects(r, '{}?next=/{}/update/'.format(
            settings.LOGIN_URL,
            BASE_URL,
        ))

    def test_authorized_user_can_view_profile_update_view(self):
        '''
        Tests authorized user can view ProfileUpdateView
        '''
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get('/{}/update/'.format(BASE_URL))
        self.assertTemplateUsed(r, 'profiles/profile_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.profile)

    def test_profile_update_view_has_accounts_formset(self):
        """
        プロフィール更新用のビューにアカウント用のフォームセットが渡されている
        かを確認します
        """
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get('/{}/update/'.format(BASE_URL))
        self.assertTrue('formset' in r.context)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update profile via ProfileUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/{}/update/'.format(BASE_URL), {
            'pub_state' : 'public',
            'place' : '札幌市北区',
            'url' : 'http://www.kawaz.org/members/kawaztan/',
            'remarks' : 'けろーん',
            'birth_day' : datetime.datetime.today()
        })
        self.assertRedirects(r, '{}?next=/{}/update/'.format(
            settings.LOGIN_URL,
            BASE_URL,
        ))
        self.assertEqual(self.profile.place, 'グランエターナ')

    def test_owner_can_update_via_update_view(self):
        '''
        プロフィールの持ち主がプロフィール更新用のビューからプロフィールを
        更新できる
        '''
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.post('/{}/update/'.format(BASE_URL), {
            'pub_state': 'public',
            'place': '札幌市北区',
            'url': 'http://www.kawaz.org/members/kawaztan/',
            'remarks': 'けろーん',
            'birth_day': datetime.datetime.today(),
            'accounts-TOTAL_FORMS': 0,  # アカウントは作成しない
            'accounts-INITIAL_FORMS': 1,
            'accounts-MAX_NUM_FORMS': 1000,
        })
        self.assertRedirects(r, '/members/{}/'.format(
            self.user.username
        ))
        self.assertEqual(Profile.objects.count(), 1)
        e = Profile.objects.get(pk=1)
        self.assertEqual(e.place, '札幌市北区')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_owner_can_update_via_update_view_with_accounts(self):
        '''
        プロフィールの持ち主がプロフィール更新用のビューから複数のアカウントを
        設定できる
        '''
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        self.assertEqual(Account.objects.count(), 0)
        r = self.client.post('/{}/update/'.format(BASE_URL), {
            'pub_state': 'public',
            'place': '札幌市北区',
            'url': 'http://www.kawaz.org/members/kawaztan/',
            'remarks': 'けろーん',
            'birth_day': datetime.datetime.today(),
            'accounts-0-service': 1,
            'accounts-0-username': '@kawaztan',
            'accounts-0-pub_state': 'public',
            'accounts-1-service': 2,
            'accounts-1-username': '@kawaztan2',
            'accounts-1-pub_state': 'public',
            'accounts-TOTAL_FORMS': 2,
            'accounts-INITIAL_FORMS': 0,
            'accounts-MAX_NUM_FORMS': 1000,
        })
        self.assertRedirects(r, '/members/{}/'.format(
            self.user.username
        ))
        self.assertEqual(Profile.objects.count(), 1)
        e = Profile.objects.get(pk=1)
        self.assertEqual(e.place, '札幌市北区')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")
        accounts = Account.objects.all()
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(accounts[0].service.pk, 1)
        self.assertEqual(accounts[0].profile.user, self.user)
        self.assertEqual(accounts[0].username, '@kawaztan')
        self.assertEqual(accounts[0].pub_state, 'public')
        self.assertEqual(accounts[1].profile.user, self.user)
        self.assertEqual(accounts[1].service.pk, 2)
        self.assertEqual(accounts[1].username, '@kawaztan2')
        self.assertEqual(accounts[1].pub_state, 'public')

    def test_account_formset(self):
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get('/{}/update/'.format(BASE_URL))
        self.assertTemplateUsed(r, 'profiles/profile_form.html')
        self.assertTrue('formset' in r.context_data)


class ProfilePreviewTestCase(TestCase):
    def test_profile_preview(self):
        """
        ユーザーが/profiles/preview/を閲覧できる
        """
        r = self.client.get("/{}/preview/".format(BASE_URL))
        self.assertTemplateUsed(r, "profiles/components/profile_detail.html")
