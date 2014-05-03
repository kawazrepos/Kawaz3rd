from django.test import TestCase
from .factories import CategoryFactory, EntryFactory

from django.contrib.auth.models import AnonymousUser

from kawaz.core.personas.tests.factories import PersonaFactory

class EventPermissionTestCase(TestCase):

    def test_author_has_change_perm(self):
        '''Tests author has change permission'''
        entry = EntryFactory()
        self.assertTrue(entry.author.has_perm('blogs.change_entry', entry))

    def test_others_do_not_have_change_perm(self):
        '''Tests others don't have change permission'''
        user = PersonaFactory()
        entry = EntryFactory()
        self.assertFalse(user.has_perm('blogs.change_entry', entry))

    def test_anonymous_do_not_have_change_perm(self):
        '''Tests an anonymous user don't have change permission'''
        user = AnonymousUser()
        entry = EntryFactory()
        self.assertFalse(user.has_perm('blogs.change_entry', entry))

    def test_author_has_delete_perm(self):
        '''Tests author has delete permission'''
        entry = EntryFactory()
        self.assertTrue(entry.author.has_perm('blogs.delete_entry', entry))

    def test_others_do_not_have_delete_perm(self):
        '''Tests others don't have delete permission'''
        user = PersonaFactory()
        entry = EntryFactory()
        self.assertFalse(user.has_perm('blogs.delete_entry', entry))

    def test_anonymous_do_not_have_delete_perm(self):
        '''Tests an anonymous user don't have delete permission'''
        user = AnonymousUser()
        entry = EntryFactory()
        self.assertFalse(user.has_perm('blogs.delete_entry', entry))

    def test_author_has_view_perm_of_draft(self):
        '''Tests author can view own draft entry'''
        user = PersonaFactory()
        entry = EntryFactory(pub_state='draft', author=user)
        self.assertTrue(user.has_perm('blogs.view_entry', entry))

    def test_other_do_not_have_view_perm_of_draft(self):
        '''Tests user can not view others draft entry'''
        user = PersonaFactory()
        entry = EntryFactory(pub_state='draft')
        self.assertFalse(user.has_perm('blogs.view_entry', entry))

    def test_authenticated_user_has_view_perm_of_protected(self):
        '''Tests authenticated user can view protected entry'''
        user = PersonaFactory()
        entry = EntryFactory(pub_state='protected')
        self.assertTrue(user.has_perm('blogs.view_entry', entry))

    def test_anonymous_user_do_not_have_view_perm_of_protected(self):
        '''Tests anonymous user can not view protected entry'''
        user = AnonymousUser()
        entry = EntryFactory(pub_state='protected')
        self.assertFalse(user.has_perm('blogs.view_entry', entry))

    def test_anonymous_user_can_view_public_entry(self):
        '''Tests an anonymous user can view public entry'''
        user = AnonymousUser()
        entry = EntryFactory(pub_state='public')
        self.assertTrue(user.has_perm('blogs.view_entry', entry))

    def test_authorized_user_can_view_public_entry(self):
        '''Tests an authorized user can view public entry'''
        user = PersonaFactory()
        entry = EntryFactory(pub_state='public')
        self.assertTrue(user.has_perm('blogs.view_entry', entry))
