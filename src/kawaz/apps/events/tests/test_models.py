import datetime
from django.utils.timezone import get_default_timezone
from unittest import mock
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Event
from ..models import Category
from .factories import EventFactory
from .factories import CategoryFactory
from .utils import static_now
from .utils import event_factory_with_relative


@mock.patch('django.utils.timezone.now', static_now)
class EventManagerTestCase(TestCase):
    def setUp(self):
        # specify standard time. it should be later than the time returned by
        # `_static_now` function.
        standard_time = static_now()
        # create event list for testing.
        arguments_list = (
                (-3, 0),                                # 2000/9/1-4
                (-2, -1),                               # 2000/9/2-3
                (4, 5),                                 # 2000/9/8-9
                (5, 6, {'pub_state': 'draft'}),         # 2000/9/9-10
                (0, 3, {'pub_state': 'protected'}),     # 2000/9/4-7
            )
        self.event_list = [event_factory_with_relative(*args)
                           for args in arguments_list]

    def test_active_with_authenticated_user(self):
        """
        active(authenticated_user) should return event queryset which only
        contain events have not finished yet and the status is public or
        protected.
        """
        # create authenticated user for getting protected events as well
        user = PersonaFactory()
        # specify authenticated user
        qs = Event.objects.active(user)

        self.assertEqual(Event.objects.count(), 5)
        self.assertEqual(qs.count(), 3)
        # event has finished (2000/9/2-3) and draft event is not appeared.
        self.assertEqual(qs[0], self.event_list[0], '2000/9/1-4')
        self.assertEqual(qs[1], self.event_list[4], '2000/9/4-7 (protected)')
        self.assertEqual(qs[2], self.event_list[2], '2000/9/8-9')

    def test_active_with_anonymous_user(self):
        """
        active(anonymous_user) should return event queryset which only
        contain events have not finished yet and the status is public.
        """
        user = AnonymousUser()

        qs = Event.objects.active(user)

        self.assertEqual(Event.objects.count(), 5)
        self.assertEqual(qs.count(), 2)
        # event has finished (2000/9/2-3) and protected or draft are not appeared.
        self.assertEqual(qs[0], self.event_list[0], '2000/9/1-4')
        self.assertEqual(qs[1], self.event_list[2], '2000/9/8-9')

    def test_published_with_authenticated_user(self):
        """
        publish(authenticated_user) should return event queryset which stats is
        protected or public
        """
        # create authenticated user for getting protected events as well
        user = PersonaFactory()
        qs = Event.objects.published(user)

        self.assertEqual(Event.objects.count(), 5)
        self.assertEqual(qs.count(), 4)
        # protected or public events are appeared
        self.assertEqual(qs[0], self.event_list[0], '2000/9/1-4')
        self.assertEqual(qs[1], self.event_list[1], '2000/9/2-3')
        self.assertEqual(qs[2], self.event_list[4], '2000/9/4-7 (protected)')
        self.assertEqual(qs[3], self.event_list[2], '2000/9/8-9')

    def test_published_with_anonymous_user(self):
        """
        publish(anonymous_user) should return event queryset which stats is
        public
        """
        user = AnonymousUser()
        qs = Event.objects.published(user)

        self.assertEqual(Event.objects.count(), 5)
        self.assertEqual(qs.count(), 3)
        # protected or public events are appeared
        self.assertEqual(qs[0], self.event_list[0], '2000/9/1-4')
        self.assertEqual(qs[1], self.event_list[1], '2000/9/2-3')
        self.assertEqual(qs[2], self.event_list[2], '2000/9/8-9')

    def test_draft_with_organizer(self):
        """
        draft(organizer) should return event queryset which contains organized
        draft events
        """
        user = self.event_list[3].organizer
        qs = Event.objects.draft(user=user)

        self.assertEqual(Event.objects.count(), 5)
        self.assertEqual(qs.count(), 1)
        # only self organized draft event is appeard
        self.assertEqual(qs[0], self.event_list[3], '2000/9/9-10')

    def test_draft_with_authenticated_user(self):
        """
        draft(authenticated_user) should not return queryset which contains
        draft events if the user does not have any organized draft events.
        """
        user = PersonaFactory()

        qs = Event.objects.draft(user)

        self.assertEqual(Event.objects.count(), 5)
        self.assertEqual(qs.count(), 0)


@mock.patch('django.utils.timezone.now', static_now)
class EventManagerAttendanceRestrictionTestCase(TestCase):
    def setUp(self):
        # specify standard time. it should be later than the time returned by
        # `_static_now` function.
        standard_time = static_now()
        attendance_deadline = standard_time - datetime.timedelta(hours=24)
        # create event list for testing.
        arguments_list = (
                (-3, 0),                                # 2000/9/1-4
                (-2, -1),                               # 2000/9/2-3
                (4, 5),                                 # 2000/9/8-9
                (5, 6, {'pub_state': 'draft'}),         # 2000/9/9-10
                (0, 3, {'pub_state': 'protected'}),     # 2000/9/4-7
                (5, 6, {'number_restriction': 1}),
                (5, 6,),
            )
        self.event_list = [event_factory_with_relative(*args)
                           for args in arguments_list]
        static_now_past = lambda: static_now() - datetime.timedelta(hours=48)
        with mock.patch('django.utils.timezone.now', static_now_past):
            self.event_list[-1].attendance_deadline = attendance_deadline
            self.event_list[-1].save()

    def test_attendable_with_authenticated_user(self):
        """
        active(authenticated_user) should return event queryset which only
        contain events have not finished yet and the status is public or
        protected.
        """
        # create authenticated user for getting protected events as well
        user = PersonaFactory()
        # specify authenticated user
        qs = Event.objects.attendable(user)

        self.assertEqual(Event.objects.count(), 7)
        self.assertEqual(qs.count(), 3)
        # event has finished (2000/9/2-3) and draft event is not appeared.
        self.assertEqual(qs[0], self.event_list[0], '2000/9/1-4')
        self.assertEqual(qs[1], self.event_list[4], '2000/9/4-7 (protected)')
        self.assertEqual(qs[2], self.event_list[2], '2000/9/8-9')

    def test_attendable_with_anonymous_user(self):
        """
        active(anonymous_user) should return event queryset which only
        contain events have not finished yet and the status is public.
        """
        user = AnonymousUser()

        qs = Event.objects.attendable(user)

        self.assertEqual(Event.objects.count(), 7)
        self.assertEqual(qs.count(), 2)
        # event has finished (2000/9/2-3) and protected or draft are not appeared.
        self.assertEqual(qs[0], self.event_list[0], '2000/9/1-4')
        self.assertEqual(qs[1], self.event_list[2], '2000/9/8-9')

class EventCategoryTest(TestCase):
    def test_str(self):
        """
        str(Category)がラベルを返します
        """
        category = CategoryFactory(label='飲み会')
        self.assertEqual(str(category), '飲み会')

    def test_order(self):
        """
        Categoryがorderの値順に並びます
        """
        CategoryFactory(label='飲み会', order=1)
        CategoryFactory(label='ゲームオフ', order=2)
        CategoryFactory(label='GameJam', order=3)

        categories = Category.objects.all()
        self.assertEqual(categories[0].label, '飲み会')
        self.assertEqual(categories[1].label, 'ゲームオフ')
        self.assertEqual(categories[2].label, 'GameJam')

@mock.patch('django.utils.timezone.now', static_now)
@override_settings(LANGUAGE_CODE='en-us')
class EventTestCase(TestCase):
    def test_str(self):
        """str(event) should return the event title"""
        event = EventFactory()
        self.assertEqual(str(event), event.title)

    def test_ordering(self):
        """
        Events should be orered by period_start, period_end, created_at,
        updated_at, and title with respecting the appearance order.
        """
        e0 = event_factory_with_relative(2, 2)
        e1 = event_factory_with_relative(1, 3)
        e2 = event_factory_with_relative(1, 2)
        e3 = event_factory_with_relative(5, 7)
        
        qs = Event.objects.all()
        self.assertEqual(qs[0], e2)
        self.assertEqual(qs[1], e1)
        self.assertEqual(qs[2], e0)
        self.assertEqual(qs[3], e3)

    def test_attend(self):
        """
        attend(user) method should add the specified user to the attendees
        """
        user = PersonaFactory()
        event = EventFactory()
        # organizer is automatically attended to the event
        self.assertEqual(event.attendees.count(), 1)
        # add new user
        event.attend(user)
        self.assertEqual(event.attendees.count(), 2)

    def test_attend_with_number_restriction(self):
        """
        """
        user = PersonaFactory()
        event = EventFactory(number_restriction=1)
        # organizer is automatically attended to the event
        self.assertEqual(event.attendees.count(), 1)
        # add new user
        self.assertRaises(PermissionDenied, event.attend, user)

    def test_attend_with_attendance_deadline(self):
        """
        """
        static_now_past = lambda: static_now() - datetime.timedelta(hours=48)
        attendance_deadline = static_now() - datetime.timedelta(hours=24)
        user = PersonaFactory()
        with mock.patch('django.utils.timezone.now', static_now_past):
            event = EventFactory(attendance_deadline=attendance_deadline)
        # organizer is automatically attended to the event
        self.assertEqual(event.attendees.count(), 1)
        # add new user
        self.assertRaises(PermissionDenied, event.attend, user)

    def test_attendees(self):
        """
        attendees should be the user queryset
        """
        user = PersonaFactory()
        event = EventFactory(organizer=user)
        # organizer attend the event automatically
        self.assertEqual(event.attendees.count(), 1)
        self.assertEqual(event.attendees.all()[0], user)
        # in case, test `in` operator
        self.assertTrue(user in event.attendees.all())

    def test_is_attendee(self):
        """
        is_attendee(user) method should return True if the specified user is in
        attendee
        """
        user1 = PersonaFactory()
        user2 = PersonaFactory()
        event = EventFactory()
        event.attend(user1)
        self.assertTrue(event.is_attendee(user1))
        self.assertFalse(event.is_attendee(user2))

    def test_organizer_attend_event_automatically(self):
        """
        Event organizer attend the event automatically
        """
        user1 = PersonaFactory()
        user2 = PersonaFactory()
        event = EventFactory(organizer=user1)
        self.assertEqual(event.organizer, user1)
        self.assertTrue(event.is_attendee(user1))
        self.assertFalse(event.is_attendee(user2))

    def test_quit(self):
        """
        quit(user) method remove the specified user from the attendee
        """
        event = EventFactory()
        user = PersonaFactory()

        # Note: organizer attend the class automatically
        event.attend(user)
        self.assertEqual(event.attendees.count(), 2)

        event.quit(user)
        self.assertEqual(event.attendees.count(), 1)
        self.assertFalse(user in user.groups.all())

    def test_is_active_with_inactive_event(self):
        """
        is_active() should return False for events which held before
        """
        standard_time = static_now()
        # create an event which just end 1 day before
        event = event_factory_with_relative(-4, -1)
        self.assertFalse(event.is_active())

    def test_is_active_with_event_have_not_started(self):
        """
        is_active() should return True for events have not started
        """
        standard_time = static_now()
        # create an event which will start just 1 hour later
        kwargs = dict(
                period_start=standard_time+datetime.timedelta(hours=1),
                period_end=standard_time+datetime.timedelta(hours=3),
            )
        event = EventFactory(**kwargs)
        self.assertTrue(event.is_active())

    def test_is_active_with_event_going(self):
        """
        is_active() should return True for events going
        """
        standard_time = static_now()
        # create an event which have started just 1 day before and end
        # just 1 day later
        event = event_factory_with_relative(-1, 1)
        self.assertTrue(event.is_active())

    def test_is_active_with_event_without_period(self):
        """
        is_active() should return True for events without period
        """
        # create an event without period_start and period_end
        kwargs = dict(
                period_start=None,
                period_end=None,
            )
        event = EventFactory(**kwargs)
        self.assertTrue(event.is_active())

    def test_get_absolute_url(self):
        """
        get_absolute_url() should return /events/pk
        """
        event = EventFactory()
        self.assertEqual(event.get_absolute_url(),
                         '/events/{0}/'.format(event.pk))

    def test_humanize_period(self):
        """
        event.humanize_periodで開始時間、終了時間が取れる
        """
        event = EventFactory()
        self.assertEqual(event.humanized_period, '09/04(Mon) 01:00 ~ 04:00')


    def test_humanize_period_other_year(self):
        """
        event.humanize_periodで開始時間、終了時間が取れる
        別の年のとき、年が表示される
        """
        now = static_now()
        event = EventFactory(period_start=now + datetime.timedelta(days=365, hours=1),
                             period_end=now + datetime.timedelta(days=365, hours=4)
        )
        self.assertEqual(event.humanized_period, '2001/09/04(Tue) 01:00 ~ 04:00')

    def test_humanize_period_unfixed(self):
        """
        event.humanize_periodで開始時間、終了時間が取れる
        開催日未定のとき、unfixedになる
        """
        event = EventFactory(period_start=None, period_end=None)
        self.assertEqual(event.humanized_period, 'Start time is unfixed')

    def test_humanize_period_end_time_unfixed(self):
        """
        event.humanize_periodで開始時間、終了時間が取れる
        終了時間が未定のとき、終了時間未定になる
        """
        event = EventFactory(period_end=None)
        self.assertEqual(event.humanized_period, '09/04(Mon) 01:00 ~ End time is unfixed')

    def test_humanize_period_otherday(self):
        """
        event.humanize_periodで開始時間、終了時間が取れる
        イベントが数日にまたがるとき、日付が表示される
        """
        now = static_now()
        event = EventFactory(period_start=now + datetime.timedelta(hours=1),
                             period_end=now + datetime.timedelta(days=2, hours=4)
        )
        self.assertEqual(event.humanized_period, '09/04(Mon) 01:00 ~ 09/06(Wed) 04:00')

@mock.patch('django.utils.timezone.now', static_now)
class EventValidationTestCase(TestCase):
    def test_organizer_cannot_quit(self):
        """
        Event organizer is not allowed to quit the event and raise
        PermissionDenied
        """
        user = PersonaFactory()
        event = EventFactory(organizer=user)
        self.assertRaises(PermissionDenied, event.quit, user)

    def test_non_attendee_cannot_quit(self):
        """
        Ofcourse non attendee cannot quit the event
        """
        user = PersonaFactory()
        event = EventFactory()
        self.assertRaises(PermissionDenied, event.quit, user)

    def test_backgoing_event_is_not_allowed(self):
        """
        Raise ValidationError when period_start is later than period_end
        """
        standard_time = static_now()
        kwargs = dict(
                period_start=standard_time+datetime.timedelta(hours=1),
                period_end=standard_time,
            )
        self.assertRaises(ValidationError, EventFactory, **kwargs)

    def test_start_time_must_be_future(self):
        """
        Raise ValidationError when the period_start is specified as a past date
        """
        standard_time = static_now()
        kwargs = dict(
                period_start=standard_time+datetime.timedelta(hours=-1),
                period_end=standard_time,
            )
        self.assertRaises(ValidationError, EventFactory, **kwargs)

    def test_event_period_cannot_be_longer_than_8_days(self):
        """
        Raise ValidationError when the event period is longer than 8 days
        """
        standard_time = static_now()
        kwargs = dict(
                period_start=standard_time,
                period_end=standard_time+datetime.timedelta(days=8),
            )
        self.assertRaises(ValidationError, EventFactory, **kwargs)

    def test_period_end_without_period_start_is_now_allowed(self):
        """
        Raise ValidationError when period_end is specified without specifing
        period_start
        """
        standard_time = static_now()
        kwargs = dict(
                period_start=None,
                period_end=standard_time,
            )
        self.assertRaises(ValidationError, EventFactory, **kwargs)

    def test_number_restriction_should_be_grater_than_zero(self):
        """
        人数制限は一人以上からしか認めない
        """
        kwargs = dict(
                number_restriction=0,
            )
        self.assertRaises(ValidationError, EventFactory, **kwargs)

    def test_attendance_deadline_must_be_future(self):
        """
        参加締め切りは未来でなければいけない
        """
        standard_time = static_now()
        kwargs = dict(
                attendance_deadline=standard_time-datetime.timedelta(hours=1),
            )
        self.assertRaises(ValidationError, EventFactory, **kwargs)
