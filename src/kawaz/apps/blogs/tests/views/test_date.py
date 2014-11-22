from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import get_default_timezone
from ..factories import EntryFactory
from kawaz.core.personas.tests.factories import PersonaFactory

def get_local_time(dt):
    tz = get_default_timezone()
    return dt.astimezone(tz)

class EntryYearArchiveViewTestCase(TestCase):
    def setUp(self):
        self.entries = (
            EntryFactory(),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='draft'),
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_can_view_only_public_entries(self):
        '''
        Tests anonymous user can view public Entry written in the year only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/blogs/{}/'.format(self.entries[0].published_at.year))
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('date_list' in r.context_data)
        list = r.context_data['date_list']
        self.assertEqual(list.count(), 1, 'date_list has one month')

    def test_wille_can_view_only_public_entries(self):
        '''
        Tests wille user can view public Entry written in the year only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/{}/'.format(self.entries[0].published_at.year))
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('date_list' in r.context_data)
        list = r.context_data['date_list']
        self.assertEqual(list.count(), 1, 'date_list has one month')

    def test_authenticated_can_view_all_publish_entries(self):
        '''
        Tests authenticated user can view all published  written in the year entries.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{}/'.format(self.entries[0].published_at.year))
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('date_list' in r.context_data)
        list = r.context_data['date_list']
        self.assertEqual(list.count(), 1, 'date_list has one month')

class EntryAuthorYearArchiveViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.entries = (
            EntryFactory(),
            EntryFactory(author=self.user),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='protected', author=self.user),
            EntryFactory(pub_state='draft'),
        )

    def test_anonymous_can_view_only_public_entries_of_the_author(self):
        '''
        Tests anonymous user can view public Entry written by specific author in the year only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/blogs/{0}/{1}/'.format(self.user.username, self.entries[0].published_at.year))
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('date_list' in r.context_data)
        list = r.context_data['date_list']
        self.assertEqual(list.count(), 1, 'date_list has one month')

    def test_wille_can_view_only_public_entries_of_the_author(self):
        '''
        Tests wille user can view public Entry written by specific author in the year only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/{0}/{1}/'.format(self.user.username, self.entries[0].published_at.year))
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('date_list' in r.context_data)
        list = r.context_data['date_list']
        self.assertEqual(list.count(), 1, 'date_list has one month')

    def test_authenticated_can_view_all_publish_entries_of_the_author(self):
        '''
        Tests authenticated user can view all published entries written by specific author in the year.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{0}/{1}/'.format(self.user.username, self.entries[0].published_at.year))
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('date_list' in r.context_data)
        list = r.context_data['date_list']
        self.assertEqual(list.count(), 1, 'date_list has one month')

class EntryMonthArchiveViewTestCase(TestCase):
    def setUp(self):
        self.entries = (
            EntryFactory(),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='draft'),
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_can_view_only_public_entries(self):
        '''
        Tests anonymous user can view public Entry written in the month only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        entry = self.entries[0]
        lt = get_local_time(entry.published_at)
        r = self.client.get('/blogs/{0}/{1}/'.format(lt.year, lt.month))
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_wille_can_view_only_public_entries(self):
        '''
        Tests wille user can view public Entry written in the month only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        entry = self.entries[0]
        lt = get_local_time(entry.published_at)
        r = self.client.get('/blogs/{0}/{1}/'.format(lt.year, lt.month))
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_authenticated_can_view_all_publish_entries(self):
        '''
        Tests authenticated user can view all published entries written in the month.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.user, password='password'))
        lt = get_local_time(entry.published_at)
        r = self.client.get('/blogs/{0}/{1}/'.format(lt.year, lt.month))
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[1], 'protected')
        self.assertEqual(list[1], self.entries[0], 'public')

class EntryAuthorMonthArchiveViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.entries = (
            EntryFactory(),
            EntryFactory(author=self.user),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='protected', author=self.user),
            EntryFactory(pub_state='draft'),
        )

    def test_anonymous_can_view_only_public_entries_of_the_author(self):
        '''
        Tests anonymous user can view public Entry written by specific author in the month only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        entry = self.entries[0]
        lt = get_local_time(entry.published_at)
        r = self.client.get('/blogs/{0}/{1}/{2}/'.format(self.user.username, lt.year, lt.month))
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_wille_can_view_only_public_entries_of_the_author(self):
        '''
        Tests wille user can view public Entry written by specific author in the month only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        entry = self.entries[0]
        lt = get_local_time(entry.published_at)
        r = self.client.get('/blogs/{0}/{1}/{2}/'.format(self.user.username, lt.year, lt.month))
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_authenticated_can_view_all_publish_entries_of_the_author(self):
        '''
        Tests authenticated user can view all published entries written by specific author in the month.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.user, password='password'))
        lt = get_local_time(entry.published_at)
        r = self.client.get('/blogs/{0}/{1}/{2}/'.format(self.user.username, lt.year, lt.month))
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[3], 'protected')
        self.assertEqual(list[1], self.entries[1], 'public')

class EntryDayArchiveViewTestCase(TestCase):
    def setUp(self):
        self.entries = (
            EntryFactory(),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='draft'),
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_can_view_only_public_entries(self):
        '''
        Tests anonymous user can view public Entry written on the day only.
        The protected entries are not displayed.
        '''
        entry = self.entries[0]
        user = AnonymousUser()
        r = self.client.get('/blogs/{0}/{1}/{2}/'.format(get_local_time(entry.published_at).year, get_local_time(entry.published_at).month, get_local_time(entry.published_at).day))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_wille_can_view_only_public_entries(self):
        '''
        Tests wille user can view public Entry written on the day only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        entry = self.entries[0]
        r = self.client.get('/blogs/{0}/{1}/{2}/'.format(get_local_time(entry.published_at).year, get_local_time(entry.published_at).month, get_local_time(entry.published_at).day))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_authenticated_can_view_all_publish_entries(self):
        '''
        Tests authenticated user can view all published entries written on the day.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{0}/{1}/{2}/'.format(get_local_time(entry.published_at).year, get_local_time(entry.published_at).month, get_local_time(entry.published_at).day))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[1], 'protected')
        self.assertEqual(list[1], self.entries[0], 'public')

class EntryAuthorDayArchiveViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.entries = (
            EntryFactory(),
            EntryFactory(author=self.user),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='protected', author=self.user),
            EntryFactory(pub_state='draft'),
        )

    def test_anonymous_can_view_only_public_entries_of_the_author(self):
        '''
        Tests anonymous user can view public Entry written by specific author on the day only.
        The protected entries are not displayed.
        '''
        entry = self.entries[0]
        r = self.client.get('/blogs/{0}/{1}/{2}/{3}/'.format(self.user.username, get_local_time(entry.published_at).year, get_local_time(entry.published_at).month, get_local_time(entry.published_at).day))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_wille_can_view_only_public_entries_of_the_author(self):
        '''
        Tests wille user can view public Entry written by specific author on the day only.
        The protected entries are not displayed.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/{0}/{1}/{2}/{3}/'.format(self.user.username, get_local_time(entry.published_at).year, get_local_time(entry.published_at).month, get_local_time(entry.published_at).day))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_authenticated_can_view_all_publish_entries_of_the_author(self):
        '''
        Tests authenticated user can view all published entries written by specific author on the day.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{0}/{1}/{2}/{3}/'.format(self.user.username, get_local_time(entry.published_at).year, get_local_time(entry.published_at).month, get_local_time(entry.published_at).day))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[3], 'protected')
        self.assertEqual(list[1], self.entries[1], 'public')


class EntryTodayArchiveViewTestCase(TestCase):
    def setUp(self):
        self.entries = (
            EntryFactory(),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='draft'),
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_can_view_only_public_entries(self):
        '''
        Tests anonymous user can view public Entry written on today only.
        The protected entries are not displayed.
        '''
        entry = self.entries[0]
        user = AnonymousUser()
        r = self.client.get('/blogs/today/')
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_wille_can_view_only_public_entries(self):
        '''
        Tests wille user can view public Entry written on today only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        entry = self.entries[0]
        r = self.client.get('/blogs/today/')
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_authenticated_can_view_all_publish_entries(self):
        '''
        Tests authenticated user can view all published entries written on today.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/today/')
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[1], 'protected')
        self.assertEqual(list[1], self.entries[0], 'public')

class EntryAuthorTodayArchiveViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.entries = (
            EntryFactory(),
            EntryFactory(author=self.user),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='protected', author=self.user),
            EntryFactory(pub_state='draft'),
        )

    def test_anonymous_can_view_only_public_entries_of_the_author(self):
        '''
        Tests anonymous user can view public Entry written by specific author on today only.
        The protected entries are not displayed.
        '''
        entry = self.entries[0]
        r = self.client.get('/blogs/{}/today/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_wille_can_view_only_public_entries_of_the_author(self):
        '''
        Tests wille user can view public Entry written by specific author on today only.
        The protected entries are not displayed.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/{}/today/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_authenticated_can_view_all_publish_entries_of_the_author(self):
        '''
        Tests authenticated user can view all published entries written by specific author on today.
        '''
        entry = self.entries[0]
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{}/today/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_archive_day.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[3], 'protected')
        self.assertEqual(list[1], self.entries[1], 'public')
