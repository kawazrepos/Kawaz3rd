from django.test import TestCase

import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from .factories import ProfileFactory
from .factories import ServiceFactory
from ..models import Profile
from ..models import Account
from kawaz.core.personas.tests.factories import PersonaFactory

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
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(profile.get_absolute_url())
        self.assertTemplateUsed(r, 'profiles/profile_detail.html')
        self.assertEqual(r.context_data['object'], profile)

    def test_anonymous_user_can_not_view_protected_profile(self):
        '''Tests anonymous user can not view protected profile'''
        profile = ProfileFactory(pub_state='protected')
        r = self.client.get(profile.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, profile.get_absolute_url()))

    def test_wille_user_can_not_view_protected_profile(self):
        '''Tests wille user can not view protected profile'''
        profile = ProfileFactory(pub_state='protected')
        self.user.role = 'wille'
        self.user.save()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(profile.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, profile.get_absolute_url()))

    def test_authorized_user_can_view_protected_profile(self):
        '''Tests authorized user can view public profile'''
        profile = ProfileFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user, password='password'))
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
        r = self.client.get('/members/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/members/update/')

    def test_authorized_user_can_view_profile_update_view(self):
        '''
        Tests authorized user can view ProfileUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/members/update/')
        self.assertTemplateUsed(r, 'profiles/profile_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.profile)

    def test_profile_update_view_has_accounts_formset(self):
        """
        プロフィール更新用のビューにアカウント用のフォームセットが渡されているかを確認します
        """
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/members/update/')
        self.assertTrue('formset' in r.context)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update profile via ProfileUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/members/update/', {
            'pub_state' : 'public',
            'place' : '札幌市北区',
            'url' : 'http://www.kawaz.org/members/kawaztan/',
            'remarks' : 'けろーん',
            'birth_day' : datetime.datetime.today()
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/members/update/')
        self.assertEqual(self.profile.place, 'グランエターナ')

    def test_owner_can_update_via_update_view(self):
        '''
        プロフィールの持ち主がプロフィール更新用のビューからプロフィールを更新できる
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/members/update/', {
            'pub_state': 'public',
            'place': '札幌市北区',
            'url': 'http://www.kawaz.org/members/kawaztan/',
            'remarks': 'けろーん',
            'birth_day': datetime.datetime.today(),
            'accounts-TOTAL_FORMS': 0,  # アカウントは作成しない
            'accounts-INITIAL_FORMS': 1,
            'accounts-MAX_NUM_FORMS': 1000,
        })
        self.assertRedirects(r, '/members/{}/'.format(self.user.username))
        self.assertEqual(Profile.objects.count(), 1)
        e = Profile.objects.get(pk=1)
        self.assertEqual(e.place, '札幌市北区')

    def test_owner_can_update_via_update_view_with_accounts(self):
        '''
        プロフィールの持ち主がプロフィール更新用のビューから複数のアカウントを設定できる
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        self.assertEqual(Account.objects.count(), 0)
        r = self.client.post('/members/update/', {
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
        self.assertRedirects(r, '/members/{}/'.format(self.user.username))
        self.assertEqual(Profile.objects.count(), 1)
        e = Profile.objects.get(pk=1)
        self.assertEqual(e.place, '札幌市北区')
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
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/members/update/')
        self.assertTemplateUsed(r, 'profiles/profile_form.html')
        self.assertTrue('formset' in r.context_data)


class ProfileListViewTestCase(TestCase):
    def setUp(self):
        self.profiles = (
            ProfileFactory(),
            ProfileFactory(user=PersonaFactory(is_active=False)),
            ProfileFactory(pub_state='protected')
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
        r = self.client.get('/members/')
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
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/members/')
        self.assertTemplateUsed('profiles/profile_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one profile')
        self.assertEqual(list[0], self.profiles[0], 'public')

    def test_authenticated_can_view_all_active_profiles(self):
        '''
        Tests authenticated user can view all active profiles.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/members/')
        self.assertTemplateUsed('profiles/profile_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two profiles')
        self.assertEqual(list[0], self.profiles[0], 'public')
        self.assertEqual(list[1], self.profiles[2], 'protected')


class ProfilePreviewTestCase(TestCase):
    def test_profile_preview(self):
        """
        ユーザーが/members/preview/を閲覧できる
        """
        r = self.client.get("/members/preview/")
        self.assertTemplateUsed(r, "profiles/components/profile_detail.html")