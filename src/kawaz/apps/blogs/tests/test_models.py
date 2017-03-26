import datetime
import urllib
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

    def test_get_absolute_url(self):
        """
        get_absolute_urlでカテゴリの記事一覧ページのURLが取得できる
        /blogs/<author>/category/<category_pk>/
        """
        category = CategoryFactory()
        self.assertEqual(category.get_absolute_url(), '/blogs/{}/category/{}/'.format(category.author.username, category.pk))


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

    def test_published_at(self):
        '''Tests published_at is set correctly'''
        entry = EntryFactory()
        self.assertIsNotNone(entry.published_at)

    def test_published_at_draft(self):
        '''Tests published_at is not set, when pub_state is draft'''
        entry = EntryFactory(pub_state='draft')
        self.assertIsNone(entry.published_at)

    def test_published_at_update(self):
        '''Tests published_at is not modified'''
        entry = EntryFactory()
        published_at = entry.published_at

        entry.pub_state = 'draft'
        entry.save()
        self.assertEqual(published_at, entry.published_at)

        entry.pub_state = 'public'
        entry.save()
        self.assertEqual(published_at, entry.published_at)

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
        published_at = datetime.datetime(2112, 9, 21, tzinfo=timezone.utc)
        entry = EntryFactory(published_at=published_at, author=user)
        self.assertEqual(entry.get_absolute_url(), '/blogs/mecha_kawaztan/2112/9/21/{}/'.format(entry.pk))

    def test_get_absolute_url_of_draft(self):
        '''
        Tests get_absolute_url of draft returns update page.
        '''
        user = PersonaFactory(username='kawaztan_kawaztan')
        entry = EntryFactory(pub_state='draft', author=user)
        self.assertEqual(entry.get_absolute_url(), '/blogs/kawaztan_kawaztan/{}/update/'.format(entry.pk))

    def test_published_at_date_property(self):
        '''
        Tests published_at_date returns datetime
        '''
        published_at = datetime.datetime(2112, 9, 21, tzinfo=timezone.utc)
        entry = EntryFactory(published_at=published_at)
        self.assertEqual(entry.published_at_date,datetime.date(2112, 9, 21))

    def test_published_at_automatically(self):
        '''
        Tests published_at is set for current time automatically
        '''
        today = timezone.now()
        entry = EntryFactory()
        self.assertEqual(entry.published_at_date, datetime.date(today.year, today.month, today.day))

    def test_published_at_is_not_set_draft(self):
        '''
        Tests published_at isn't set when pub_state is draft
        '''
        entry = EntryFactory(pub_state='draft')
        self.assertIsNone(entry.published_at)
        self.assertIsNone(entry.published_at_date)

    def test_published_at_is_not_updated(self):
        '''
        Tests published_at isn't updated, this value never change.
        '''
        entry = EntryFactory()
        old_published_at = entry.published_at
        entry.pub_state = 'draft'
        entry.save()
        self.assertEqual(entry.published_at, old_published_at)
        entry.pub_state = 'public'
        entry.save()
        self.assertEqual(entry.published_at, old_published_at)
