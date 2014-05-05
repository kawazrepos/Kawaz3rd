import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from ..factories import EntryFactory
from ...models import Entry
from kawaz.core.personas.tests.factories import PersonaFactory

class EntryDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_view_public_entry(self):
        '''Tests anonymous user can view public entry'''
        entry = EntryFactory()
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_detail.html')
        self.assertEqual(r.context_data['object'], entry)

    def test_authorized_user_can_view_public_entry(self):
        '''Tests authorized user can view public entry'''
        entry = EntryFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_detail.html')
        self.assertEqual(r.context_data['object'], entry)

    def test_anonymous_user_can_not_view_protected_entry(self):
        '''Tests anonymous user can not view protected entry'''
        entry = EntryFactory(pub_state='protected')
        r = self.client.get(entry.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, entry.get_absolute_url()))

    def test_authorized_user_can_view_protected_entry(self):
        '''Tests authorized user can view public entry'''
        entry = EntryFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_detail.html')
        self.assertEqual(r.context_data['object'], entry)

    def test_anonymous_user_can_not_view_draft_entry(self):
        '''Tests anonymous user can not view draft entry'''
        entry = EntryFactory(pub_state='draft')
        r = self.client.get(entry.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, entry.get_absolute_url()))

    def test_others_can_not_view_draft_entry(self):
        '''
        Tests others can not view draft entry
        User will redirect to '/entries/1/update/'
        '''
        entry = EntryFactory(pub_state='draft')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/{}/1/update/'.format(entry.author.username))

    def test_organizer_can_view_draft_entry(self):
        '''Tests organizer can view draft entry on update view'''
        entry = EntryFactory(pub_state='draft', author=self.user)
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_form.html')
        self.assertEqual(r.context_data['object'], entry)

class EntryCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_not_create_view(self):
        '''Tests anonymous user can not view EntryCreateView'''
        r = self.client.get('/blogs/{}/create/'.format(self.user.username))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/{}/create/'.format(self.user.username))

    def test_authorized_user_can_view_entry_create_view(self):
        '''Tests authorized user can view EntryCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{}/create/'.format(self.user.username))
        self.assertTemplateUsed(r, 'blogs/entry_form.html')
        self.assertFalse('object' in r.context_data)

    def test_anonymous_user_can_not_create_via_create_view(self):
        '''Tests anonymous user can not create entry via EntryCreateView'''
        r = self.client.post('/blogs/{}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/{}/create/'.format(self.user.username))

    def test_authorized_user_can_create_via_create_view(self):
        '''Tests authorized user can create entry via EntryCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/{}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
        })
        today = datetime.date.today()
        self.assertRedirects(r, '/blogs/{0}/{1}/{2}/{3}/1/'.format(self.user.username, today.year, today.month, today.day))
        self.assertEqual(Entry.objects.count(), 1)
        e = Entry.objects.get(pk=1)
        self.assertEqual(e.title, '日記です')

    def test_user_cannot_modify_author_id(self):
        '''
        Tests authorized user cannot modify author id.
        In entry creation form, `author` is exist as hidden field.
        So user can modify `author` to invalid values.
        This test checks that `author` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/{0}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
            'author' : other.pk # crackers attempt to masquerade
        })
        today = datetime.date.today()
        self.assertRedirects(r, '/blogs/{0}/{1}/{2}/{3}/1/'.format(self.user.username, today.year, today.month, today.day))
        self.assertEqual(Entry.objects.count(), 1)
        e = Entry.objects.get(pk=1)
        self.assertEqual(e.author, self.user)
        self.assertNotEqual(e.author, other)


class EntryUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='author_kawaztan')
        self.user.set_password('password')
        self.other = PersonaFactory(username='black_kawaztan')
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.entry = EntryFactory(title='かわずたんだよ☆', author=self.user)

    def test_anonymous_user_can_not_view_entry_update_view(self):
        '''Tests anonymous user can not view EntryUpdateView'''
        r = self.client.get('/blogs/author_kawaztan/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/1/update/')

    def test_authorized_user_can_view_entry_update_view(self):
        '''
        Tests authorized user can view EntryUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/author_kawaztan/1/update/')
        self.assertTemplateUsed(r, 'blogs/entry_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.entry)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update entry via EntryUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/blogs/author_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'クラッカーだよー',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/1/update/')
        self.assertEqual(self.entry.title, 'かわずたんだよ☆')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update entry via EntryUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/blogs/author_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'いたずら日記です',
            'body' : '黒かわずたんだよーん',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/1/update/')
        self.assertEqual(self.entry.title, 'かわずたんだよ☆')

    def test_author_can_update_via_update_view(self):
        '''Tests author user can update entry via EntryUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/author_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, '/blogs/author_kawaztan/{0}/{1}/{2}/1/'.format(self.entry.publish_at.year, self.entry.publish_at.month, self.entry.publish_at.day))
        self.assertEqual(Entry.objects.count(), 1)
        e = Entry.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')

    def test_user_cannot_modify_author_id(self):
        '''
        Tests authorized user cannot modify author id.
        In entry update form, `author` is exist as hidden field.
        So user can modify `author` to invalid values.
        This test checks that `author` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/author_kawaztan/1/update/', {
            'pub_state' : 'public',
            'title' : 'ID書き換えます！',
            'body' : 'うえーい',
            'author' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/blogs/author_kawaztan/{0}/{1}/{2}/1/'.format(self.entry.publish_at.year, self.entry.publish_at.month, self.entry.publish_at.day))
        self.assertEqual(Entry.objects.count(), 1)
        e = Entry.objects.get(pk=1)
        self.assertEqual(e.author, self.user)
        self.assertNotEqual(e.author, other)
        self.assertEqual(e.title, 'ID書き換えます！')

class EntryListViewTestCase(TestCase):
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
        Tests anonymous user can view public Entry only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/blogs/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_wille_can_view_only_public_entries(self):
        '''
        Tests wille user can view public Entry only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_authenticated_can_view_all_publish_entries(self):
        '''
        Tests authenticated user can view all published entries.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[1], 'protected')
        self.assertEqual(list[1], self.entries[0], 'public')

class EntryAuthorListViewTestCase(TestCase):
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
        Tests anonymous user can view public Entry written by specific author only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_wille_can_view_only_public_entries_of_the_author(self):
        '''
        Tests wille user can view public Entry written by specific author only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])

    def test_authenticated_can_view_all_publish_entries_of_the_author(self):
        '''
        Tests authenticated user can view all published entries written by specific author.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertEqual(list[0], self.entries[3], 'protected')
        self.assertEqual(list[1], self.entries[1], 'public')
