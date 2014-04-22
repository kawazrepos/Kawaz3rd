from django.test import TestCase

import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from .factories import ProfileFactory
from ..models import Profile
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.tests.datetime import patch_datetime_now

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
        '''Tests authorized user can update profile via ProfileUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/members/update/', {
            'pub_state' : 'public',
            'place' : '札幌市北区',
            'url' : 'http://www.kawaz.org/members/kawaztan/',
            'remarks' : 'けろーん',
            'birth_day' : datetime.datetime.today()
        })
        self.assertRedirects(r, '/members/{}/'.format(self.user.username))
        self.assertEqual(Profile.objects.count(), 1)
        e = Profile.objects.get(pk=1)
        self.assertEqual(e.place, '札幌市北区')

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
