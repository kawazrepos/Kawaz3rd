from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .factories import CategoryFactory, EntryFactory

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
