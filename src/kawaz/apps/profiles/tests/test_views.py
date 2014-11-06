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


class ProfileDetailViewTestCase(TestCase):

    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_view_public_profile(self):
        '''Tests anonymous user can view public profile'''
        profile = ProfileFactory()
        r = self.client.get(profile.get_absolute_url())
        self.assertTemplateUsed(r, 'profiles/profile_detail.html')
        self.assertEqual(r.context_data['object'], profile)

    def test_authorized_user_can_view_public_profile(self):
        '''Tests authorized user can view public profile'''
        profile = ProfileFactory()
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get(profile.get_absolute_url())
        self.assertTemplateUsed(r, 'profiles/profile_detail.html')
        self.assertEqual(r.context_data['object'], profile)

    def test_anonymous_user_can_not_view_protected_profile(self):
        '''Tests anonymous user can not view protected profile'''
        profile = ProfileFactory(pub_state='protected')
        r = self.client.get(profile.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(
            settings.LOGIN_URL, profile.get_absolute_url()
        ))

    def test_wille_user_can_not_view_protected_profile(self):
        '''Tests wille user can not view protected profile'''
        profile = ProfileFactory(pub_state='protected')
        self.user.role = 'wille'
        self.user.save()
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get(profile.get_absolute_url())
        self.assertRedirects(r, '{}?next={}'.format(
            settings.LOGIN_URL, profile.get_absolute_url()
        ))

    def test_authorized_user_can_view_protected_profile(self):
        '''Tests authorized user can view public profile'''
        profile = ProfileFactory(pub_state='protected')
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get(profile.get_absolute_url())
        self.assertTemplateUsed(r, 'profiles/profile_detail.html')
        self.assertEqual(r.context_data['object'], profile)


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
        self.assertRedirects(r, '/{}/{}/'.format(
            BASE_URL,
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
        self.assertRedirects(r, '/{}/{}/'.format(
            BASE_URL,
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


class ProfileListViewTestCase(TestCase):
    def setUp(self):
        self.profiles = (
            ProfileFactory(user__last_login=datetime.datetime(
                2000, 1, 1, tzinfo=get_default_timezone()
            )),
            ProfileFactory(user=PersonaFactory(is_active=False)),
            ProfileFactory(pub_state='protected',
                           user__last_login=datetime.datetime(
                               2001, 1, 1, tzinfo=get_default_timezone()
                           ))
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_can_view_only_public_profiles(self):
        '''
        Tests anonymous user can view public Profiles only.
        The protected profiles are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/{}/'.format(BASE_URL))
        self.assertTemplateUsed('profiles/profile_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one profile')
        self.assertEqual(list[0], self.profiles[0], 'public')

    def test_wille_can_view_all_active_profiles(self):
        '''
        Tests wille user can view public Profiles only.
        The protected profiles are not displayed.
        '''
        self.user.role = 'wille'
        self.user.save()
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get('/{}/'.format(BASE_URL))
        self.assertTemplateUsed('profiles/profile_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one profile')
        self.assertEqual(list[0], self.profiles[0], 'public')

    def test_authenticated_can_view_all_active_profiles(self):
        '''
        ログインユーザーが全てのユーザーが見れる、かつ最近ログイン順に並ぶ
        '''
        self.assertTrue(self.client.login(
            username=self.user, password='password'
        ))
        r = self.client.get('/{}/'.format(BASE_URL))
        self.assertTemplateUsed('profiles/profile_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two profiles')
        self.assertEqual(list[0], self.profiles[2], 'protected')
        self.assertEqual(list[1], self.profiles[0], 'public')


class ProfilePreviewTestCase(TestCase):
    def test_profile_preview(self):
        """
        ユーザーが/profiles/preview/を閲覧できる
        """
        r = self.client.get("/{}/preview/".format(BASE_URL))
        self.assertTemplateUsed(r, "profiles/components/profile_detail.html")
