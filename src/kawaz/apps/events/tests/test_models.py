import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser

from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import EventFactory


class EventTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct values'''
        event = EventFactory()
        self.assertEqual(event.__str__(), event.title)

    def test_attend(self):
        '''Tests can attend correctly'''
        user = PersonaFactory()
        event = EventFactory()
        self.assertEqual(event.attendees.count(), 1)

        event.attend(user)

        self.assertEqual(event.attendees.count(), 2)

    def test_is_attendee(self):
        '''Tests is_attendee returns correct value'''
        user = PersonaFactory()
        user2 = PersonaFactory()
        event = EventFactory(organizer=user)
        self.assertEqual(event.attendees.count(), 1)
        self.assertEqual(event.attendees.all()[0], user)
        self.assertTrue(event.is_attendee(user))
        self.assertFalse(event.is_attendee(user2))

    def test_organizer_is_attendee(self):
        '''Tests organizer will be attend automatically'''
        user = PersonaFactory()
        event = EventFactory(organizer=user)
        self.assertTrue(event.is_attendee(user))

    def test_quit(self):
        '''Tests can remove member correctly'''
        event = EventFactory()
        user = PersonaFactory()

        event.attend(user)
        self.assertEqual(event.attendees.count(), 2)

        event.quit(user)
        self.assertEqual(event.attendees.count(), 1)
        self.assertFalse(user in user.groups.all())

    def test_organizer_cant_quit(self):
        '''Tests organizer can't quit from events'''
        organizer = PersonaFactory()
        event = EventFactory(organizer=organizer)

        self.assertRaises(PermissionDenied, event.quit, organizer)

    def test_not_attendee_cant_quit(self):
        '''Tests non attendee can't quit from events'''
        event = EventFactory()
        user = PersonaFactory()

        self.assertRaises(PermissionDenied, event.quit, user)

    def test_later_than_start_time(self):
        '''Tests end time must be later than start time'''
        now = datetime.datetime.now()
        start = now + datetime.timedelta(hours=6)
        end = now + datetime.timedelta(hours=4)

        self.assertRaises(ValidationError, EventFactory, period_start=start, period_end=end)

    def test_same_between_start_and_end_time(self):
        '''Tests end time can be allowed same with start time'''
        now = datetime.datetime.now()
        start = now + datetime.timedelta(hours=5)
        end = now + datetime.timedelta(hours=5)

        self.assertIsNotNone(EventFactory(period_start=start, period_end=end))

    def test_start_time_must_be_future(self):
        '''Tests start time must be future'''
        now = datetime.datetime.now()
        start_time = now + datetime.timedelta(hours=-5)
        end_time = now + datetime.timedelta(hours=5)

        self.assertRaises(ValidationError, EventFactory, period_start=start_time, period_end=end_time)

    def test_event_period_is_too_long(self):
        '''Tests period of event must be shorter than 8 days'''
        now = datetime.datetime.now()
        start = now + datetime.timedelta(days=1)
        end = now + datetime.timedelta(days=9)

        self.assertRaises(ValidationError, EventFactory, period_start=start, period_end=end)

        # period of event that is under 8 days is allowed (Kawaz 2nd)
        start2 = now + datetime.timedelta(days=1)
        end2 = now + datetime.timedelta(days=9, seconds=-1)
        self.assertIsNotNone(EventFactory(period_start=start2, period_end=end2))

    def test_set_only_end_time(self):
        '''Tests event must not only have end time.'''
        now = datetime.datetime.now()
        end = now + datetime.timedelta(days=8)

        self.assertRaises(ValidationError, EventFactory, period_start=None, period_end=end)

    def test_is_active(self):
        '''Tests is_active returns correct value'''

        # ToDo stubbing datetime.datetime.now()
        now = datetime.datetime.now()
        start = now + datetime.timedelta(hours=1)
        end = now + datetime.timedelta(hours=4)
        event = EventFactory.build(period_start=start, period_end=end)
        self.assertTrue(event.is_active())

        start2 = now + datetime.timedelta(hours=-4)
        end2 = now + datetime.timedelta(hours=-1)
        event2 = EventFactory.build(period_start=start2, period_end=end2)
        self.assertFalse(event2.is_active())

        start3 = now + datetime.timedelta(hours=-4)
        end3 = now + datetime.timedelta(hours=1)
        event3 = EventFactory.build(period_start=start3, period_end=end3)
        self.assertTrue(event3.is_active())

        event4 = EventFactory.build(period_start=None, period_end=None)
        self.assertTrue(event4.is_active())

    def test_organizer_can_edit(self):
        '''Tests organizer can edit an event'''
        event = EventFactory()
        self.assertTrue(event.organizer.has_perm('events.change_event', event))

    def test_others_can_not_edit(self):
        '''Tests others can no edit an event'''
        user = PersonaFactory()
        event = EventFactory()
        self.assertFalse(user.has_perm('events.change_event', event))

    def test_anonymous_can_not_edit(self):
        '''Tests anonymous user can no edit an event'''
        user = AnonymousUser()
        event = EventFactory()
        self.assertFalse(user.has_perm('events.change_event', event))

    def test_organizer_can_delete(self):
        '''Tests organizer can delete an event'''
        event = EventFactory()
        self.assertTrue(event.organizer.has_perm('events.delete_event', event))

    def test_others_can_not_delete(self):
        '''Tests others can not delete an event'''
        user = PersonaFactory()
        event = EventFactory()
        self.assertFalse(user.has_perm('events.delete_event', event))

    def test_anonymous_can_not_delete(self):
        '''Tests anonymous users can not delete an event'''
        user = AnonymousUser()
        event = EventFactory()
        self.assertFalse(user.has_perm('events.delete_event', event))

    def test_organizer_can_view_draft(self):
        '''Tests organizer can view draft'''
        event = EventFactory(pub_state='draft')
        self.assertTrue(event.organizer.has_perm('events.view_event', event))

    def test_others_can_not_view_draft(self):
        '''Tests others can not view draft'''
        user = PersonaFactory()
        event = EventFactory(pub_state='draft')
        self.assertFalse(user.has_perm('events.view_event', event))

    def test_anonymous_can_not_view_draft(self):
        '''Tests anonymous can not view draft'''
        user = AnonymousUser()
        event = EventFactory(pub_state='draft')
        self.assertFalse(user.has_perm('events,view_event', event))

    def test_organizer_can_view_protected(self):
        '''Tests organizer can view protected'''
        event = EventFactory(pub_state='protected')
        self.assertTrue(event.organizer.has_perm('events.view_event', event))

    def test_others_can_view_protected(self):
        '''Tests others can view protected'''
        user = PersonaFactory()
        event = EventFactory(pub_state='protected')
        self.assertTrue(user.has_perm('events.view_event', event))

    def test_anonymous_can_not_view_protected(self):
        '''Tests anonymous can not view protected'''
        user = AnonymousUser()
        event = EventFactory(pub_state='protected')
        self.assertFalse(user.has_perm('events,view_event', event))

    def test_organizer_can_view_public(self):
        '''Tests organizer can view public'''
        event = EventFactory(pub_state='public')
        self.assertTrue(event.organizer.has_perm('events.view_event', event))

    def test_others_can_view_public(self):
        '''Tests others can view public'''
        user = PersonaFactory()
        event = EventFactory(pub_state='public')
        self.assertTrue(user.has_perm('events.view_event', event))

    def test_anonymous_can_not_view_public(self):
        '''Tests anonymous can view public'''
        user = AnonymousUser()
        event = EventFactory(pub_state='public')
        self.assertTrue(user.has_perm('events.view_event', event))
