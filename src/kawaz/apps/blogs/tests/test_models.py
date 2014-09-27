import datetime
from django.utils import timezone
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
        self.assertEqual(qs[0], self.entries[1])
        self.assertEqual(qs[1], self.entries[0])

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
        qs = Entry.objects.draft(self.entries[2].author)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], self.entries[2])

    def test_draft_with_other(self):
        '''Tests Entry.objects.draft() with owner user returns all own draft entries'''
        user = PersonaFactory()
        qs = Entry.objects.draft(user)
        self.assertEqual(qs.count(), 0)


class EntryModelTestCase(TestCase):
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

    def test_get_absolute_url(self):
        '''
        Tests get_absolute_url returns /<author>/<year>/<month>/<day>/<pk>/
        '''
        user = PersonaFactory(username='mecha_kawaztan')
        publish_at = datetime.datetime(2112, 9, 21, tzinfo=timezone.utc)
        entry = EntryFactory(publish_at=publish_at, author=user)
        self.assertEqual(entry.get_absolute_url(), '/blogs/mecha_kawaztan/2112/9/21/1/')

    def test_get_absolute_url_of_draft(self):
        '''
        Tests get_absolute_url of draft returns update page.
        '''
        user = PersonaFactory(username='kawaztan_kawaztan')
        entry = EntryFactory(pub_state='draft', author=user)
        self.assertEqual(entry.get_absolute_url(), '/blogs/kawaztan_kawaztan/1/update/')

    def test_publish_at_date_property(self):
        '''
        Tests publish_at_date returns datetime
        '''
        publish_at = datetime.datetime(2112, 9, 21, tzinfo=timezone.utc)
        entry = EntryFactory(publish_at=publish_at)
        self.assertEqual(entry.publish_at_date,datetime.date(2112, 9, 21))

    def test_publish_at_automatically(self):
        '''
        Tests publish_at is set for current time automatically
        '''
        today = timezone.datetime.today()
        entry = EntryFactory()
        self.assertEqual(entry.publish_at_date, datetime.date(today.year, today.month, today.day))

    def test_publish_at_is_not_set_draft(self):
        '''
        Tests publish_at isn't set when pub_state is draft
        '''
        entry = EntryFactory(pub_state='draft')
        self.assertIsNone(entry.publish_at)
        self.assertIsNone(entry.publish_at_date)

    def test_publish_at_is_not_updated(self):
        '''
        Tests publish_at isn't updated, this value never change.
        '''
        entry = EntryFactory()
        old_publish_at = entry.publish_at
        entry.pub_state = 'draft'
        entry.save()
        self.assertEqual(entry.publish_at, old_publish_at)
        entry.pub_state = 'public'
        entry.save()
        self.assertEqual(entry.publish_at, old_publish_at)
