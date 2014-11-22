from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from ...models import Profile
from ...models import ProfileManager
from ..factories import PersonaFactory
from ..factories import ProfileFactory
from ..factories import SkillFactory
from ..factories import AccountFactory
from ..factories import ServiceFactory


class ProfileManagerTestCase(TestCase):

    def setUp(self):
        self.active_profile = ProfileFactory()
        self.inactive_profile = ProfileFactory(user=PersonaFactory(is_active=False))
        self.protected_profile = ProfileFactory(pub_state='protected')
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_register_profile_manager(self):
        '''
        Tests Profile.objects returns ProfileManager object
        '''
        self.assertTrue(type(Profile.objects), ProfileManager)

    def test_active(self):
        '''
        Tests Profile.objects.active() returns QuerySet which contains active user only.
        '''
        qs = Profile.objects.active()
        self.assertEqual(qs.count(), 2, 'Queryset have two personas')
        self.assertEqual(qs[0], self.active_profile, 'Queryset have active profile')
        self.assertEqual(qs[1], self.protected_profile, 'Queryset have active profile')

    def test_published_with_authorized(self):
        '''
        Tests Profile.objects.published() returns QuerySet which contains all active users
        when passed authorized user as its argument.
        '''
        qs = Profile.objects.published(self.user)
        self.assertEqual(qs.count(), 2, 'Queryset have two personas')
        self.assertEqual(qs[0], self.active_profile, 'Queryset have public profile')
        self.assertEqual(qs[1], self.protected_profile, 'Queryset have internal profile')

    def test_published_with_wille(self):
        '''
        Tests Profile.objects.published() returns QuerySet which contains public users
        when passed users whose role is `wille` as its argument.
        '''
        qs = Profile.objects.published(self.wille)
        self.assertEqual(qs.count(), 1, 'Queryset have one profile')
        self.assertEqual(qs[0], self.active_profile, 'Queryset have public profile')

    def test_published_with_anonymous(self):
        '''
        Tests Profile.objects.published() returns QuerySet which contains public users
        when passed anonymous user as its argument.
        '''
        qs = Profile.objects.published(self.anonymous)
        self.assertEqual(qs.count(), 1, 'Queryset have one profile')
        self.assertEqual(qs[0], self.active_profile, 'Queryset have public profile')


class ProfileTestCase(TestCase):

    def test_str(self):
        '''Tests __str__ returns correct value'''
        persona = PersonaFactory(nickname='kawaz tan')
        profile = ProfileFactory(user=persona)
        self.assertEqual(str(profile), 'kawaz tan')

    def test_create_user(self):
        """Tests can access profile via user.get_profile()"""
        profile = ProfileFactory()
        self.assertEqual(profile.user._profile, profile)


class ProfileAuthorPermissionTestCase(TestCase):

    def test_owner_can_edit(self):
        '''Tests owner can edit an profile'''
        profile = ProfileFactory()
        self.assertTrue(profile.user.has_perm('personas.change_profile', profile))

    def test_others_can_not_edit(self):
        '''Tests others can no edit an profile'''
        user = PersonaFactory()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('personas.change_profile', profile))

    def test_anonymous_can_not_edit(self):
        '''Tests anonymous user can no edit an profile'''
        user = AnonymousUser()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('personas.change_profile', profile))

    def test_owner_can_not_delete(self):
        '''Tests owner can not delete an profile'''
        profile = ProfileFactory()
        self.assertFalse(profile.user.has_perm('personas.delete_profile', profile))

    def test_others_can_not_delete(self):
        '''Tests others can not delete an profile'''
        user = PersonaFactory()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('personas.delete_profile', profile))

    def test_anonymous_can_not_delete(self):
        '''Tests anonymous users can not delete an profile'''
        user = AnonymousUser()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('personas.delete_profile', profile))


class SkillTestCase(TestCase):
    def test_str(self):
        """Tests __str__ returns correct value"""
        skill = SkillFactory()
        self.assertEqual(str(skill), skill.label)

class ServiceTestCase(TestCase):
    def test_str(self):
        """Tests __str__ returns correct value"""
        service = ServiceFactory()
        self.assertEqual(str(service), service.label)

class AccountTestCase(TestCase):
    def test_get_url(self):
        """Tests can get URL from property"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(account.url, 'http://twitter.com/kawaz_tan/')

    def test_test(self):
        """Tests __str__ returns correct value"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(str(account), '{} ({} @ {})'.format(
            account.username,
            account.profile.user.username,
            account.service.label)
        )
