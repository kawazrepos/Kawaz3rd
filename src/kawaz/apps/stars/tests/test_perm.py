from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Star
from .factories import StarFactory

class StarAddPermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_users_have_add_star_permission(self):
        '''
        Tests users have permission to add stars
        '''
        self.assertTrue(self.user.has_perm('stars.add_star'))

    def test_wille_dont_have_add_star_permission(self):
        '''
        Tests wille users do not have permission to add stars
        '''
        self.assertFalse(self.wille.has_perm('stars.add_star'))

    def test_anonymous_dont_have_add_star_permission(self):
        '''
        Tests anonymous users do not have permission to add stars
        '''
        self.assertFalse(self.anonymous.has_perm('stars.add_star'))


class StarChangePermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()
        self.star = StarFactory()

    def test_users_dont_have_change_star_permission(self):
        '''
        Tests users do not have permission to change stars
        '''
        self.assertFalse(self.user.has_perm('stars.change_star'))

    def test_wille_dont_have_change_star_permission(self):
        '''
        Tests wille users do not have permission to change stars
        '''
        self.assertFalse(self.wille.has_perm('stars.change_star'))

    def test_anonymous_dont_have_change_star_permission(self):
        '''
        Tests anonymous users do not have permission to change stars
        '''
        self.assertFalse(self.anonymous.has_perm('stars.change_star'))

    def test_users_dont_have_change_star_permission_with_object(self):
        '''
        Tests users do not have permission to change specific star
        '''
        self.assertFalse(self.user.has_perm('stars.change_star', obj=self.star))

    def test_author_dont_have_change_permission(self):
        '''
        Tests onwers have permission to delete own star
        '''
        self.assertFalse(self.star.author.has_perm('stars.change_star', obj=self.star))

    def test_wille_dont_have_change_star_permission_with_object(self):
        '''
        Tests wille users do not have permission to change specific star
        '''
        self.assertFalse(self.wille.has_perm('stars.change_star', obj=self.star))

    def test_anonymous_dont_have_change_star_permission_with_object(self):
        '''
        Tests anonymous users do not have permission to change specific star
        '''
        self.assertFalse(self.anonymous.has_perm('stars.change_star', obj=self.star))


class StarDeletePermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()
        self.star = StarFactory()

    def test_users_have_delete_star_permission(self):
        '''
        Tests users do not have permission to delete stars
        '''
        self.assertTrue(self.user.has_perm('stars.delete_star'))

    def test_wille_dont_have_delete_star_permission(self):
        '''
        Tests wille users do not have permission to delete stars
        '''
        self.assertFalse(self.wille.has_perm('stars.delete_star'))

    def test_anonymous_dont_have_delete_star_permission(self):
        '''
        Tests anonymous users do not have permission to delete stars
        '''
        self.assertFalse(self.anonymous.has_perm('stars.delete_star'))

    def test_users_dont_have_delete_star_permission_with_object(self):
        '''
        Tests users do not have permission to delete specific star
        '''
        self.assertFalse(self.user.has_perm('stars.delete_star', obj=self.star))

    def test_author_have_delete_permission(self):
        '''
        Tests onwers have permission to delete own star
        '''
        self.assertTrue(self.star.author.has_perm('stars.delete_star', obj=self.star))

    def test_wille_dont_have_delete_star_permission_with_object(self):
        '''
        Tests wille users do not have permission to delete specific star
        '''
        self.assertFalse(self.wille.has_perm('stars.delete_star', obj=self.star))

    def test_anonymous_dont_have_delete_star_permission_with_object(self):
        '''
        Tests anonymous users do not have permission to delete specific star
        '''
        self.assertFalse(self.anonymous.has_perm('stars.delete_star', obj=self.star))