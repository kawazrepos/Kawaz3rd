from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import ProfileFactory, AccountFactory, ServiceFactory, SkillFactory

class ProfileTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        persona = PersonaFactory(nickname='kawaz tan')
        profile = ProfileFactory(user=persona)
        self.assertEqual(profile.__str__(), 'kawaz tan')

    def test_create_user(self):
        """Tests can access profile via user.get_profile()"""
        profile = ProfileFactory()
        self.assertEqual(profile.user.profile, profile)

class ProfileAuthorPermissionTestCase(TestCase):
    def test_owner_can_edit(self):
        '''Tests owner can edit an profile'''
        profile = ProfileFactory()
        self.assertTrue(profile.user.has_perm('profiles.change_profile', profile))

    def test_others_can_not_edit(self):
        '''Tests others can no edit an profile'''
        user = PersonaFactory()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('profiles.change_profile', profile))

    def test_anonymous_can_not_edit(self):
        '''Tests anonymous user can no edit an profile'''
        user = AnonymousUser()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('profiles.change_profile', profile))

    def test_owner_can_not_delete(self):
        '''Tests owner can not delete an profile'''
        profile = ProfileFactory()
        self.assertFalse(profile.user.has_perm('profiles.delete_profile', profile))

    def test_others_can_not_delete(self):
        '''Tests others can not delete an profile'''
        user = PersonaFactory()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('profiles.delete_profile', profile))

    def test_anonymous_can_not_delete(self):
        '''Tests anonymous users can not delete an profile'''
        user = AnonymousUser()
        profile = ProfileFactory()
        self.assertFalse(user.has_perm('profiles.delete_profile', profile))

class ProfileViewPermissionTestCase(TestCase):
    def test_owner_can_view_protected(self):
        '''Tests owner can view protected'''
        profile = ProfileFactory(pub_state='protected')
        self.assertTrue(profile.user.has_perm('profiles.view_profile', profile))

    def test_others_can_view_protected(self):
        '''Tests others can view protected'''
        user = PersonaFactory()
        profile = ProfileFactory(pub_state='protected')
        self.assertTrue(user.has_perm('profiles.view_profile', profile))

    def test_anonymous_can_not_view_protected(self):
        '''Tests anonymous can not view protected'''
        user = AnonymousUser()
        profile = ProfileFactory(pub_state='protected')
        self.assertFalse(user.has_perm('profiles.view_profile', profile))

    def test_owner_can_view_public(self):
        '''Tests owner can view public'''
        profile = ProfileFactory(pub_state='public')
        self.assertTrue(profile.user.has_perm('profiles.view_profile', profile))

    def test_others_can_view_public(self):
        '''Tests others can view public'''
        user = PersonaFactory()
        profile = ProfileFactory(pub_state='public')
        self.assertTrue(user.has_perm('profiles.view_profile', profile))

    def test_anonymous_can_not_view_public(self):
        '''Tests anonymous can view public'''
        user = AnonymousUser()
        profile = ProfileFactory(pub_state='public')
        self.assertTrue(user.has_perm('profiles.view_profile', profile))

class SkillTestCase(TestCase):
    def test_str(self):
        """Tests __str__ returns correct value"""
        skill = SkillFactory()
        self.assertEqual(skill.__str__(), skill.label)

class ServiceTestCase(TestCase):
    def test_str(self):
        """Tests __str__ returns correct value"""
        service = ServiceFactory()
        self.assertEqual(service.__str__(), service.label)

class AccountTestCase(TestCase):
    def test_get_url(self):
        """Tests can get URL from property"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(account.url, 'http://twitter.com/kawaz_tan/')

    def test_test(self):
        """Tests __str__ returns correct value"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(account.__str__(), '%s (%s @ %s)' % (account.username, account.user.username, account.service.label))
