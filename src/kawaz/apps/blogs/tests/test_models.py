from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .factories import CategoryFactory, EntryFactory

from django.contrib.auth.models import AnonymousUser

from kawaz.core.auth.tests.factories import UserFactory

class CategoryTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        category = CategoryFactory(label='日記')
        username = category.author.username
        self.assertEqual(category.__str__(), '日記(%s)' % username)

    def test_unique_together(self):
        '''Tests unique_together works correctly'''
        user = UserFactory()
        category = CategoryFactory(label='独り言', author=user)

        def create_duplicate():
            CategoryFactory(label='独り言', author=user)
        self.assertRaises(IntegrityError, create_duplicate)

class EntryTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        entry = EntryFactory()
        self.assertEqual(entry.__str__(), entry.title)

    def test_publish_at(self):
        '''Tests publish_at is set correctly'''
        entry = EntryFactory()
        self.assertIsNotNone(entry.publish_at)

    def test_publish_at_draft(self):
        '''Tests publish_at is not set, when pub_state is draft'''
        entry = EntryFactory(pub_state='draft')
        self.assertIsNone(entry.publish_at)

    def test_publish_at_update(self):
        '''Tests publish_at is not modified'''
        entry = EntryFactory()
        publish_at = entry.publish_at

        entry.pub_state = 'draft'
        entry.save()
        self.assertEqual(publish_at, entry.publish_at)

        entry.pub_state = 'public'
        entry.save()
        self.assertEqual(publish_at, entry.publish_at)

    def test_category_must_be_owned(self):
        '''Tests category must be owned by author'''
        user = UserFactory()
        category = CategoryFactory(author=user)

        def create():
            EntryFactory(category=category)
        self.assertRaises(ValidationError, create)

    def test_author_has_change_perm(self):
        '''Tests author has change permission'''
        entry = EntryFactory()
        self.assertTrue(entry.author.has_perm('blogs.change_entry', entry))

    def test_others_do_not_have_change_perm(self):
        '''Tests others don't have change permission'''
        user = UserFactory()
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
        user = UserFactory()
        entry = EntryFactory()
        self.assertFalse(user.has_perm('blogs.delete_entry', entry))

    def test_anonymous_do_not_have_delete_perm(self):
        '''Tests an anonymous user don't have delete permission'''
        user = AnonymousUser()
        entry = EntryFactory()
        self.assertFalse(user.has_perm('blogs.delete_entry', entry))

    def test_author_has_view_perm_of_draft(self):
        '''Tests author can view own draft entry'''
        user = UserFactory()
        entry = EntryFactory(pub_state='draft', author=user)
        self.assertTrue(user.has_perm('blogs.view_entry', entry))

    def test_other_do_not_have_view_perm_of_draft(self):
        '''Tests user can not view others draft entry'''
        user = UserFactory()
        entry = EntryFactory(pub_state='draft')
        self.assertFalse(user.has_perm('blogs.view_entry', entry))

    def test_authenticated_user_has_view_perm_of_protected(self):
        '''Tests authenticated user can view protected entry'''
        user = UserFactory()
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
        user = UserFactory()
        entry = EntryFactory(pub_state='public')
        self.assertTrue(user.has_perm('blogs.view_entry', entry))
