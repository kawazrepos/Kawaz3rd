from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .factories import CategoryFactory, EntryFactory

from django.contrib.auth.models import AnonymousUser

from kawaz.core.personas.tests.factories import PersonaFactory

from ..models import Entry
from ..models import EntryManager

class CategoryTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        category = CategoryFactory(label='日記')
        username = category.author.username
        self.assertEqual(category.__str__(), '日記(%s)' % username)

    def test_unique_together(self):
        '''Tests unique_together works correctly'''
        user = PersonaFactory()
        category = CategoryFactory(label='独り言', author=user)

        def create_duplicate():
            CategoryFactory(label='独り言', author=user)
        self.assertRaises(IntegrityError, create_duplicate)


class EntryManagerTestCase(TestCase):

    def setUp(self):
        self.entries = (
            EntryFactory(),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='draft'),
            EntryFactory(pub_state='draft'),
        )

    def test_entry_manager_is_assigned(self):
        '''Tests Entry.objects returns EntryManager instance'''
        self.assertEqual(type(Entry.objects), EntryManager)

    def test_published_with_authenticated(self):
        '''Tests Entry.objects.published() with authenticated user returns all publish entries '''
        user = PersonaFactory()
        qs = Entry.objects.published(user)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0], self.entries[0])
        self.assertEqual(qs[1], self.entries[2])

    def test_published_with_wille(self):
        '''Tests Entry.objects.published() with wille user returns only public entries '''
        user = PersonaFactory(role='wille')
        qs = Entry.objects.published(user)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], self.entries[0])

    def test_published_with_anonymous(self):
        '''Tests Entry.objects.published() with anonymous user returns only public entries '''
        user = AnonymousUser()
        qs = Entry.objects.published(user)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], self.entries[0])

    def test_draft_with_owner(self):
        '''Tests Entry.objects.published() with authenticated user returns all publish entries '''
        qs = Entry.objects.published(self.entries[2].author)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], self.entries[2])

    def test_draft_with_other(self):
        '''Tests Entry.objects.draft() with owner user returns all own draft entries'''
        user = PersonaFactory()
        qs = Entry.objects.published(user)
        self.assertEqual(qs.count(), 0)


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
        user = PersonaFactory()
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
