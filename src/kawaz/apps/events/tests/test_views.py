import datetime
from unittest import mock
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import EventFactory
from ..models import Event
from .utils import static_now
from .utils import event_factory_with_relative

# Notice
# Test cases for EventDeleteView, EventJoinView, EventQuitView have not be implemented.
# Because these views will be replaced to API.

class EventDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_view_public_event(self):
        '''Tests anonymous user can view public event'''
        event = EventFactory()
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_detail.html')
        self.assertEqual(r.context_data['object'], event)

    def test_authorized_user_can_view_public_event(self):
        '''Tests authorized user can view public event'''
        event = EventFactory()
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_detail.html')
        self.assertEqual(r.context_data['object'], event)

    def test_anonymous_user_can_not_view_protected_event(self):
        '''Tests anonymous user can not view protected event'''
        event = EventFactory(pub_state='protected')
        r = self.client.get(event.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(
            settings.LOGIN_URL, event.get_absolute_url()))

    def test_authorized_user_can_view_protected_event(self):
        '''Tests authorized user can view public event'''
        event = EventFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_detail.html')
        self.assertEqual(r.context_data['object'], event)

    def test_anonymous_user_can_not_view_draft_event(self):
        '''Tests anonymous user can not view draft event'''
        event = EventFactory(pub_state='draft')
        r = self.client.get(event.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(
            settings.LOGIN_URL, event.get_absolute_url()))

    def test_others_can_not_view_draft_event(self):
        '''
        Tests others can not view draft event
        User will redirect to '/events/1/update/'
        '''
        event = EventFactory(pub_state='draft')
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/events/1/update/')

    def test_organizer_can_view_draft_event(self):
        '''Tests organizer can view draft event on update view'''
        event = EventFactory(pub_state='draft', organizer=self.user)
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_form.html')
        self.assertEqual(r.context_data['object'], event)


class EventCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_not_view_event_create_view(self):
        '''Tests anonymous user can not view EventCreateView'''
        r = self.client.get('/events/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/events/create/')

    def test_authorized_user_can_view_event_create_view(self):
        '''Tests authorized user can view EventCreateView'''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/create/')
        self.assertTemplateUsed(r, 'events/event_form.html')
        self.assertFalse('object' in r.context_data)

    def test_anonymous_user_can_not_create_via_create_view(self):
        '''Tests anonymous user can not create event via EventCreateView'''
        r = self.client.post('/events/create/', {
            'pub_state': 'public',
            'title': 'テストイベント',
            'body': 'うえーい',
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3),
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/events/create/')

    def test_authorized_user_can_create_via_create_view(self):
        '''Tests authorized user can create event via EventCreateView'''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.post('/events/create/', {
            'pub_state' : 'public',
            'title' : 'テストイベント',
            'body' : 'うえーい',
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3)
        })
        self.assertRedirects(r, '/events/1/')
        self.assertEqual(Event.objects.count(), 1)
        e = Event.objects.get(pk=1)
        self.assertEqual(e.title, 'テストイベント')

    def test_user_cannot_modify_organizer_id(self):
        '''
        Tests authorized user cannot modify organizer id.
        In event creation form, `organizer` is exist as hidden field.
        So user can modify `organizer` to invalid values.
        This test checks that `organizer` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.post('/events/create/', {
            'pub_state' : 'public',
            'title' : 'テストイベント',
            'body' : 'うえーい',
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3),
            'organizer' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/events/1/')
        self.assertEqual(Event.objects.count(), 1)
        e = Event.objects.get(pk=1)
        self.assertEqual(e.organizer, self.user)
        self.assertNotEqual(e.organizer, other)


class EventUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.other = PersonaFactory()
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.event = EventFactory(title='変更前のイベントです',
                                  organizer=self.user)

    def test_anonymous_user_can_not_view_event_update_view(self):
        '''Tests anonymous user can not view EventUpdateView'''
        r = self.client.get('/events/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/events/1/update/')

    def test_authorized_user_can_view_event_update_view(self):
        '''
        Tests authorized user can view EventUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/1/update/')
        self.assertTemplateUsed(r, 'events/event_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.event)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update event via EventUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/events/1/update/', {
            'pub_state': 'public',
            'title': '変更後のイベントです',
            'body': 'うえーい',
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3),
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/events/1/update/')
        self.assertEqual(self.event.title, '変更前のイベントです')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update event via EventUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other,
                                          password='password'))
        r = self.client.post('/events/1/update/', {
            'pub_state': 'public',
            'title': '変更後のイベントです',
            'body': 'うえーい',
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3)
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/events/1/update/')
        self.assertEqual(self.event.title, '変更前のイベントです')

    def test_organizer_can_update_via_update_view(self):
        '''Tests authorized user can update event via EventUpdateView'''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.post('/events/1/update/', {
            'pub_state': 'public',
            'title': '変更後のイベントです',
            'body': 'うえーい',
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3)
        })
        self.assertRedirects(r, '/events/1/')
        self.assertEqual(Event.objects.count(), 1)
        e = Event.objects.get(pk=1)
        self.assertEqual(e.title, '変更後のイベントです')

    def test_user_cannot_modify_organizer_id(self):
        '''
        Tests authorized user cannot modify organizer id.
        In event update form, `organizer` is exist as hidden field.
        So user can modify `organizer` to invalid values.
        This test checks that `organizer` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.post('/events/1/update/', {
            'pub_state': 'public',
            'title': '変更後のイベントです',
            'body': 'うえーい',
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3),
            'organizer': other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/events/1/')
        self.assertEqual(Event.objects.count(), 1)
        e = Event.objects.get(pk=1)
        self.assertEqual(e.organizer, self.user)
        self.assertNotEqual(e.organizer, other)
        self.assertEqual(e.title, '変更後のイベントです')


@mock.patch('django.utils.timezone.now', static_now)
class EventListViewTestCase(TestCase):
    def setUp(self):
        arguments_list = (
            (-3, -2, {'pub_state':'public'}), # 2000/9/1 ~ 2000/9/2
            (1, 2, {'pub_state':'public'}), # 2000/9/5 ~ 2000/9/6
            (-2, -1, {'pub_state':'protected'}), # 2000/9/3 ~ 2000/9/4
            (0, 1, {'pub_state':'protected'}), # 2000/9/4 ~ 2000/9/5
            (-3, -2, {'pub_state':'draft'}), # 2000/9/2 ~ 2000/9/3
            (1, 2, {'pub_state':'draft'}), # 2000/9/5 ~ 2000/9/6
        )
        self.events = [event_factory_with_relative(*args)
                       for args in arguments_list]
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_can_view_only_public_events(self):
        '''
        Tests anonymous user can view public Events only.
        The protected events are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/events/')
        self.assertTemplateUsed('events/event_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one event')
        self.assertEqual(list[0], self.events[1], '2000/9/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_events(self):
        '''
        Tests authenticated user can view all published events.
        '''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/')
        self.assertTemplateUsed('events/event_list.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two events')
        self.assertEqual(list[0], self.events[3], '2000/9/5 ~ 6 protected')
        self.assertEqual(list[1], self.events[1], '2000/9/5 ~ 6 public')


@mock.patch('django.utils.timezone.now', static_now)
class EventMonthListViewTestCase(TestCase):
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
        self.events = [event_factory_with_relative(*args)
                       for args in arguments_list]
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_can_view_only_public_events(self):
        '''
        Tests anonymous user can view public Events only via EventMonthListView.
        The protected events are not displayed.
        The ended events are also displayed.
        '''
        r = self.client.get('/events/archive/2000/9/')
        self.assertTemplateUsed('events/event_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two events')
        self.assertEqual(list[0], self.events[0], '2000/9/1 ~ 2 public')
        self.assertEqual(list[1], self.events[1], '2000/9/5 ~ 6 public')

    def test_anonymous_can_view_only_public_events_other_month(self):
        '''
        Tests anonymous user can view public Events only via EventMonthListView.
        The protected events are not displayed.
        The ended events are also displayed.
        '''
        r = self.client.get('/events/archive/2000/10/')
        self.assertTemplateUsed('events/event_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one event')
        self.assertEqual(list[0], self.events[2], '2000/10/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_events(self):
        '''
        Tests authenticated user can view all published events via
        EventMonthListView.
        '''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/archive/2000/9/')
        self.assertTemplateUsed('events/event_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 4, 'object_list has four events')
        self.assertEqual(list[0], self.events[0], '2000/9/1 ~ 2 public')
        self.assertEqual(list[1], self.events[3], '2000/9/2 ~ 3 protected')
        self.assertEqual(list[2], self.events[4], '2000/9/4 ~ 5 protected')
        self.assertEqual(list[3], self.events[1], '2000/9/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_events_other_month(self):
        '''
        Tests authenticated user can view all published events via
        EventMonthListView.
        '''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/archive/2000/10/')
        self.assertTemplateUsed('events/event_archive_month.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two events')
        self.assertEqual(list[0], self.events[2], '2000/10/5 ~ 6 public')
        self.assertEqual(list[1], self.events[5], '2000/10/6 ~ 7 protected')


@mock.patch('django.utils.timezone.now', static_now)
class EventYearListViewTestCase(TestCase):
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
        self.events = [event_factory_with_relative(*args)
                       for args in arguments_list]
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_can_view_only_public_events(self):
        '''
        Tests anonymous user can view public Events only via EventYearListView.
        The protected events are not displayed.
        The ended events are also displayed.
        '''
        r = self.client.get('/events/archive/2000/')
        self.assertTemplateUsed('events/event_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two events')
        self.assertEqual(list[0], self.events[0], '2000/9/5 ~ 6 public')
        self.assertEqual(list[1], self.events[1], '2000/9/1 ~ 2 public')

    def test_anonymous_can_view_only_public_events_other_year(self):
        '''
        Tests anonymous user can view public Events only via EventYearListView.
        The protected events are not displayed.
        The ended events are also displayed.
        '''
        r = self.client.get('/events/archive/2001/')
        self.assertTemplateUsed('events/event_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one event')
        self.assertEqual(list[0], self.events[2], '2001/9/5 ~ 6 public')

    def test_authenticated_can_view_all_publish_events(self):
        '''
        Tests authenticated user can view all published events via
        EventYearListView.
        '''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/archive/2000/')
        self.assertTemplateUsed('events/event_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 4, 'object_list has four events')
        self.assertEqual(list[0], self.events[0], '2000/9/5 ~ 6 public')
        self.assertEqual(list[1], self.events[3], '2000/9/5 ~ 6 protected')
        self.assertEqual(list[2], self.events[4], '2000/9/2 ~ 3 public')
        self.assertEqual(list[3], self.events[1], '2000/9/2 ~ 3 protected')

    def test_authenticated_can_view_all_publish_events_other_year(self):
        '''
        Tests authenticated user can view all published events via
        EventYearListView.
        '''
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/archive/2001/')
        self.assertTemplateUsed('events/event_archive_year.html')
        self.assertTrue('object_list', r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two events')
        self.assertEqual(list[0], self.events[2], '2001/9/6 ~ 7 protected')
        self.assertEqual(list[1], self.events[5], '2001/9/4 ~ 5 public')

class EventPreviewTestCase(TestCase):
    def test_event_preview(self):
        """
        events_event_previewが表示できる
        """
        r = self.client.get('/events/preview/')
        self.assertTemplateUsed(r, 'events/components/event_detail.html')
        self.assertEqual(r.status_code, 200)
