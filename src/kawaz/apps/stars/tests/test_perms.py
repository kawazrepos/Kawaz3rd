from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.apps.blogs.tests.factories import EntryFactory
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
        self.entry =  EntryFactory()
        self.anonymous = AnonymousUser()
        self.star = StarFactory(content_object=self.entry)

    def test_users_have_delete_star_permission(self):
        '''
        Tests users have permission to delete stars
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

    def test_others_dont_have_delete_star_permission_with_object(self):
        '''
        Tests others do not have permission to delete specific star
        '''
        self.assertFalse(self.user.has_perm('stars.delete_star', obj=self.star))

    def test_content_object_owner_have_delete_star_permission_with_object(self):
        '''
        Tests owner of content object also have permission to delete specific star
        '''
        self.assertTrue(self.entry.author.has_perm('stars.delete_star', obj=self.star))

    def test_author_have_delete_permission_with_object(self):
        '''
        Tests star owners have permission to delete own star
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

class StarViewPermissionTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.entry =  EntryFactory()
        self.protectedEntry =  EntryFactory(pub_state='protected')
        self.anonymous = AnonymousUser()
        self.star = StarFactory(content_object=self.entry)
        self.protectedStar = StarFactory(content_object=self.protectedEntry)

    def test_users_have_view_star_permission(self):
        '''
        Tests users have permission to view stars
        '''
        self.assertTrue(self.user.has_perm('stars.view_star'))

    def test_wille_have_view_star_permission(self):
        '''
        Tests wille users have permission to view stars
        '''
        self.assertTrue(self.wille.has_perm('stars.view_star'))

    def test_anonymous_have_view_star_permission(self):
        '''
        Tests anonymous users have permission to view stars
        '''
        self.assertTrue(self.anonymous.has_perm('stars.view_star'))

    def test_authorized_have_view_star_permission_of_public_object(self):
        '''
        Tests authorized users have permission to view specific star assigned to public object
        '''
        self.assertTrue(self.user.has_perm('stars.view_star', obj=self.star))

    def test_author_have_view_permission_of_public_object(self):
        '''
        Tests star owners have permission to view own star
        '''
        self.assertTrue(self.star.author.has_perm('stars.view_star', obj=self.star))

    def test_wille_have_view_star_permission_of_public_object(self):
        '''
        Tests wille users have permission to view specific star assigned to public object
        '''
        self.assertTrue(self.wille.has_perm('stars.view_star', obj=self.star))

    def test_anonymous_have_view_star_permission_of_public_object(self):
        '''
        Tests anonymous users have permission to view specific star assigned to public object
        '''
        self.assertTrue(self.anonymous.has_perm('stars.view_star', obj=self.star))

    def test_authorized_have_view_star_permission_of_protected_object(self):
        '''
        Tests authorized users have permission to view specific star assigned to protected object
        '''
        self.assertTrue(self.user.has_perm('stars.view_star', obj=self.protectedStar))

    def test_author_have_view_permission_of_protected_object(self):
        '''
        Tests star owners have permission to view own star
        '''
        self.assertTrue(self.protectedStar.author.has_perm('stars.view_star', obj=self.protectedStar))

    def test_wille_dont_have_view_star_permission_of_protected_object(self):
        '''
        Tests wille users don't have permission to view specific star assigned to protected object
        '''
        self.assertFalse(self.wille.has_perm('stars.view_star', obj=self.protectedStar))

    def test_anonymous_dont_have_view_star_permission_of_protected_object(self):
        '''
        Tests anonymous users don't have permission to view specific star assigned to protected object
        '''
        self.assertFalse(self.anonymous.has_perm('stars.view_star', obj=self.protectedStar))