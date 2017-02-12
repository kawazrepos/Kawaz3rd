import datetime
from unittest import mock
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from kawaz.core.tests.testcases.views import BaseViewPermissionTestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import EventFactory, CategoryFactory
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
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

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
        self.assertTrue('messages' in r.cookies, "No messages are appeared")


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
            'attendees': [self.user.pk,],
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
            'attendees': [self.user.pk,],
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
            'attendees': [self.user.pk,],
            'period_start': datetime.datetime.now()+datetime.timedelta(hours=1),
            'period_end': datetime.datetime.now()+datetime.timedelta(hours=3)
        })
        self.assertRedirects(r, '/events/1/')
        self.assertEqual(Event.objects.count(), 1)
        e = Event.objects.get(pk=1)
        self.assertEqual(e.title, '変更後のイベントです')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

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
            'attendees': [self.user.pk],
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
        self.assertTrue('messages' in r.cookies, "No messages are appeared")


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

    def test_list_with_categories(self):
        """
        イベントリストでCategoryのfilterが有効になっている
        """
        category = CategoryFactory()
        event1 = EventFactory(category=category)
        event2 = EventFactory()
        self.assertTrue(self.client.login(username=self.user,
                                          password='password'))
        r = self.client.get('/events/?category={}'.format(category.pk))
        self.assertTemplateUsed(r, 'events/event_list.html')
        self.assertEqual(r.context['filter'].qs.count(), 1)
        self.assertTrue(event1 in r.context['filter'].qs)


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

class EventPreviewViewTestCase(TestCase):
    def test_event_preview(self):
        """
        events_event_previewが表示できる
        """
        import json
        r = self.client.post('/events/preview/', json.dumps({}), content_type='application/json')
        self.assertTemplateUsed(r, 'events/components/event_detail.html')
        self.assertEqual(r.status_code, 200)

class EventCalendarViewTestCase(BaseViewPermissionTestCase):
    def test_everyone_can_download_public_ical(self):
        """
         全てのユーザーはpublicなiCalをダウンロードできる
        """
        e = EventFactory(pub_state='public')
        for user in self.members + self.non_members:
            self.prefer_login(user)
            r = self.client.get('/events/{}/calendar/'.format(e.pk))
            self.assertEqual(r.status_code, 200)

    def test_member_can_download_private_ical(self):
        """
        メンバーはprotectedなiCalをダウンロードできる
        非メンバーの場合はログインページにリダイレクトされる
        """
        e = EventFactory(pub_state='protected')
        url = '/events/{}/calendar/'.format(e.pk)
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, url))

    def test_can_reverse_events_event_calendar(self):
        """
        URL `events_event_calendar` は`/events/<pk>/calendar/`を返す
        """
        e = EventFactory()
        self.assertEqual(reverse('events_event_calendar', kwargs={'pk': e.pk}), '/events/{}/calendar/'.format(e.pk))

    def test_cannot_get_ical_with_draft(self):
        """
        pub_state = 'draft'のEventを取得しようとしたとき、404を返す
        """
        e = EventFactory(pub_state='draft')
        self.prefer_login(e.organizer)
        r = self.client.get('/events/{}/calendar/'.format(e.pk))
        self.assertEqual(r.status_code, 404)

    def test_cannot_get_ical_with_not_period_start(self):
        """
        period_startが設定されていないEventを取得しようとしたとき、404を返す
        """
        e = EventFactory(period_start=None, period_end=None)
        r = self.client.get('/events/{}/calendar/'.format(e.pk))
        self.assertEqual(r.status_code, 404)

    def test_can_download_ical(self):
        """
        iCal形式のファイルをダウンロードできる
        """
        e = EventFactory()
        r = self.client.get('/events/{}/calendar/'.format(e.pk))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Disposition'], 'attachment; filename={}.ics'.format(e.pk))
        self.assertEqual(r['content-type'], 'text/calendar')

    def test_can_download_valid_ical(self):
        """
        正しい形式のiCalファイルをダウンロードできる
        """
        from icalendar import Calendar
        from icalendar import vDatetime, vText
        e = EventFactory()
        user = PersonaFactory()
        e.attend(user)
        e.save()

        r = self.client.get('/events/{}/calendar/'.format(e.pk))
        for content in r.streaming_content:
            cal = Calendar.from_ical(content)
            self.assertEqual(cal['version'], '2.0')
            self.assertEqual(cal['PRODID'], 'Kawaz')
            for component in cal.walk():
                if component.name == 'VEVENT':
                    self.assertEqual(component['summary'], e.title)
                    self.assertEqual(component['description'], e.body)
                    self.assertEqual(component['location'], e.place)
                    self.assertEqual(component['dtstamp'].to_ical(), vDatetime(e.created_at).to_ical())
                    self.assertEqual(component['dtstart'].to_ical(), vDatetime(e.period_start).to_ical())
                    self.assertEqual(component['dtend'].to_ical(), vDatetime(e.period_end).to_ical())
                    self.assertEqual(component['class'].to_ical(), vText('PUBLIC').to_ical())
                    self.assertEqual(component['organizer'].params['cn'], e.organizer.nickname)
                    self.assertEqual(component['organizer'].params['role'], e.organizer.role)
                    # ATENDEEがセットされている
                    for attendee, cal_attendee in zip(e.attendees.all(), component['attendee']):
                        self.assertEqual(cal_attendee.params['cn'], attendee.nickname)
                        self.assertEqual(cal_attendee.params['role'], attendee.role)
