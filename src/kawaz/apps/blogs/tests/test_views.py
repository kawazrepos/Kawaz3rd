import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from .factories import EntryFactory
from ..models import Entry
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.tests.datetime import patch_datetime_now

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
        User will redirect to '/entrys/1/update/'
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
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.other = PersonaFactory()
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.entry = EntryFactory(title='変更前のイベントです', organizer=self.user)

    def test_anonymous_user_can_not_view_entry_update_view(self):
        '''Tests anonymous user can not view EntryUpdateView'''
        r = self.client.get('/entrys/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/entrys/1/update/')

    def test_authorized_user_can_view_entry_update_view(self):
        '''
        Tests authorized user can view EntryUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/entrys/1/update/')
        self.assertTemplateUsed(r, 'blogs/entry_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.entry)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update entry via EntryUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/entrys/1/update/', {
            'pub_state' : 'public',
            'title' : '変更後のイベントです',
            'body' : 'うえーい',
            'period_start' : datetime.datetime.now() + datetime.timedelta(hours=1),
            'period_end' : datetime.datetime.now() + datetime.timedelta(hours=3),
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/entrys/1/update/')
        self.assertEqual(self.entry.title, '変更前のイベントです')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update entry via EntryUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/entrys/1/update/', {
            'pub_state' : 'public',
            'title' : '変更後のイベントです',
            'body' : 'うえーい',
            'period_start' : datetime.datetime.now() + datetime.timedelta(hours=1),
            'period_end' : datetime.datetime.now() + datetime.timedelta(hours=3)
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/entrys/1/update/')
        self.assertEqual(self.entry.title, '変更前のイベントです')

    def test_organizer_can_update_via_update_view(self):
        '''Tests authorized user can update entry via EntryUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/entrys/1/update/', {
            'pub_state' : 'public',
            'title' : '変更後のイベントです',
            'body' : 'うえーい',
            'period_start' : datetime.datetime.now() + datetime.timedelta(hours=1),
            'period_end' : datetime.datetime.now() + datetime.timedelta(hours=3)
        })
        self.assertRedirects(r, '/entrys/1/')
        self.assertEqual(Entry.objects.count(), 1)
        e = Entry.objects.get(pk=1)
        self.assertEqual(e.title, '変更後のイベントです')

    def test_user_cannot_modify_organizer_id(self):
        '''
        Tests authorized user cannot modify organizer id.
        In entry update form, `organizer` is exist as hidden field.
        So user can modify `organizer` to invalid values.
        This test checks that `organizer` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/entrys/1/update/', {
            'pub_state' : 'public',
            'title' : '変更後のイベントです',
            'body' : 'うえーい',
            'period_start' : datetime.datetime.now() + datetime.timedelta(hours=1),
            'period_end' : datetime.datetime.now() + datetime.timedelta(hours=3),
            'organizer' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/entrys/1/')
        self.assertEqual(Entry.objects.count(), 1)
        e = Entry.objects.get(pk=1)
        self.assertEqual(e.organizer, self.user)
        self.assertNotEqual(e.organizer, other)
        self.assertEqual(e.title, '変更後のイベントです')

class EntryListViewTestCase(TestCase):
    def setUp(self):
        arguments_list = (
            (-3, -2, {'pub_state':'public'}), # 2000/9/1 ~ 2000/9/2
            (1, 2, {'pub_state':'public'}), # 2000/9/5 ~ 2000/9/6
            (-2, -1, {'pub_state':'protected'}), # 2000/9/3 ~ 2000/9/4
            (0, 1, {'pub_state':'protected'}), # 2000/9/4 ~ 2000/9/5
            (-3, -2, {'pub_state':'draft'}), # 2000/9/2 ~ 2000/9/3
            (1, 2, {'pub_state':'draft'}), # 2000/9/5 ~ 2000/9/6
        )
        self.entrys = [entry_factory_with_relative(*args) for args in arguments_list]
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_can_view_only_public_entrys(self):
        '''
        Tests anonymous user can view public Entrys only.
        The protected entrys are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/entrys/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entrys[1], '2000/9/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_entrys(self):
        '''
        Tests authenticated user can view all published entrys.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/entrys/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entrys')
        self.assertEqual(list[0], self.entrys[3], '2000/9/5 ~ 6 protected')
        self.assertEqual(list[1], self.entrys[1], '2000/9/5 ~ 6 public')

class EntryMonthListViewTestCase(TestCase):
    def setUp(self):
        arguments_list = (
            (-3, -2, {'pub_state':'public'}), # 2000/9/1 ~ 2000/9/2
            (1, 2, {'pub_state':'public'}), # 2000/9/5 ~ 2000/9/6
            (31, 32, {'pub_state':'public'}), # 2000/10/5 ~ 2000/10/6
            (-2, -1, {'pub_state':'protected'}), # 2000/9/2 ~ 2000/9/3
            (0, 1, {'pub_state':'protected'}), # 2000/9/4 ~ 2000/9/5
            (32, 33, {'pub_state':'protected'}), # 2000/10/6 ~ 2000/10/7
            (-3, -2, {'pub_state':'draft'}), # 2000/9/2 ~ 2000/9/3
            (1, 2, {'pub_state':'draft'}), # 2000/9/5 ~ 2000/9/6
        )
        self.entrys = [entry_factory_with_relative(*args) for args in arguments_list]
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_can_view_only_public_entrys(self):
        '''
        Tests anonymous user can view public Entrys only via EntryMonthListView.
        The protected entrys are not displayed.
        The ended entrys are also displayed.
        '''
        r = self.client.get('/entrys/archive/2000/9/')
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entrys')
        self.assertEqual(list[0], self.entrys[0], '2000/9/1 ~ 2 public')
        self.assertEqual(list[1], self.entrys[1], '2000/9/5 ~ 6 public')

    def test_anonymous_can_view_only_public_entrys_other_month(self):
        '''
        Tests anonymous user can view public Entrys only via EntryMonthListView.
        The protected entrys are not displayed.
        The ended entrys are also displayed.
        '''
        r = self.client.get('/entrys/archive/2000/10/')
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entrys[2], '2000/10/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_entrys(self):
        '''
        Tests authenticated user can view all published entrys via EntryMonthListView.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/entrys/archive/2000/9/')
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 4, 'object_list has four entrys')
        self.assertEqual(list[0], self.entrys[0], '2000/9/1 ~ 2 public')
        self.assertEqual(list[1], self.entrys[3], '2000/9/2 ~ 3 protected')
        self.assertEqual(list[2], self.entrys[4], '2000/9/4 ~ 5 protected')
        self.assertEqual(list[3], self.entrys[1], '2000/9/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_entrys_other_month(self):
        '''
        Tests authenticated user can view all published entrys via EntryMonthListView.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/entrys/archive/2000/10/')
        self.assertTemplateUsed('blogs/entry_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entrys')
        self.assertEqual(list[0], self.entrys[2], '2000/10/5 ~ 6 public')
        self.assertEqual(list[1], self.entrys[5], '2000/10/6 ~ 7 protected')

class EntryYearListViewTestCase(TestCase):
    def setUp(self):
        arguments_list = (
            (-3, -2, {'pub_state':'public'}), # 2000/9/1 ~ 2000/9/2
            (1, 2, {'pub_state':'public'}), # 2000/9/5 ~ 2000/9/6
            (365, 366, {'pub_state':'public'}), # 2001/9/5 ~ 2001/9/6
            (-2, -1, {'pub_state':'protected'}), # 2000/9/2 ~ 2000/9/3
            (0, 3, {'pub_state':'protected'}), # 2000/9/4 ~ 2000/9/5
            (367, 368, {'pub_state':'protected'}), # 2001/9/7 ~ 2001/9/8
            (-3, -2, {'pub_state':'draft'}), # 2000/9/2 ~ 2000/9/3
            (1, 2, {'pub_state':'draft'}), # 2000/9/5 ~ 2000/9/6
        )
        self.entrys = [entry_factory_with_relative(*args) for args in arguments_list]
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_can_view_only_public_entrys(self):
        '''
        Tests anonymous user can view public Entrys only via EntryYearListView.
        The protected entrys are not displayed.
        The ended entrys are also displayed.
        '''
        r = self.client.get('/entrys/archive/2000/')
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entrys')
        self.assertEqual(list[0], self.entrys[0], '2000/9/5 ~ 6 public')
        self.assertEqual(list[1], self.entrys[1], '2000/9/1 ~ 2 public')

    def test_anonymous_can_view_only_public_entrys_other_year(self):
        '''
        Tests anonymous user can view public Entrys only via EntryYearListView.
        The protected entrys are not displayed.
        The ended entrys are also displayed.
        '''
        r = self.client.get('/entrys/archive/2001/')
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entrys[2], '2001/9/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_entrys(self):
        '''
        Tests authenticated user can view all published entrys via EntryYearListView.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/entrys/archive/2000/')
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 4, 'object_list has four entrys')
        self.assertEqual(list[0], self.entrys[0], '2000/9/5 ~ 6 public')
        self.assertEqual(list[1], self.entrys[3], '2000/9/5 ~ 6 protected')
        self.assertEqual(list[2], self.entrys[4], '2000/9/2 ~ 3 public')
        self.assertEqual(list[3], self.entrys[1], '2000/9/2 ~ 3 protected')

    def test_authenticated_can_view_all_publish_entrys_other_year(self):
        '''
        Tests authenticated user can view all published entrys via EntryYearListView.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/entrys/archive/2001/')
        self.assertTemplateUsed('blogs/entry_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entrys')
        self.assertEqual(list[0], self.entrys[2], '2001/9/6 ~ 7 protected')
        self.assertEqual(list[1], self.entrys[5], '2001/9/4 ~ 5 public')