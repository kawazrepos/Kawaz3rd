from django.test import TestCase
from Kawaz.apps.auth.tests.factories import UserFactory
from ..models import Event
from .factories import EventFactory

class EventTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct values'''
        event = EventFactory()
        self.assertEqual(event.__str__(), event.title)

    def test_attend(self):
        '''Tests can attend correctly'''
        user = UserFactory()
        event = EventFactory()
        self.assertEqual(event.attendees.count(), 1)

        event.attend(user)

        self.assertEqual(event.attendees.count(), 2)

    def test_is_attendee(self):
        '''Tests is_attendee returns correct value'''
        user = UserFactory()
        user2 = UserFactory()
        event = EventFactory(organizer=user)
        self.assertEqual(event.attendees.count(), 1)
        self.assertEqual(event.attendees.all()[0], user)
        self.assertTrue(event.is_attendee(user))
        self.assertFalse(event.is_attendee(user2))

    def test_organizer_is_attendee(self):
        '''Tests organizer will be attend automatically'''
        user = UserFactory()
        event = EventFactory(organizer=user)
        self.assertTrue(event.is_attendee(user))

    def test_quit(self):
        '''Tests can remove member correctly'''
        event = EventFactory()
        user = UserFactory()

        event.attend(user)
        self.assertEqual(event.attendees.count(), 2)

        event.quit(user)
        self.assertEqual(event.attendees.count(), 1)
        self.assertFalse(user in user.groups.all())

    def test_organizer_cant_quit(self):
        '''Tests organizer can't quit from events'''
        event = EventFactory()

        def quit():
            event.quit(event.organizer)
        self.assertRaises(AttributeError, quit)

    def test_not_attendee_cant_quit(self):
        '''Tests non attendee can't quit from events'''
        event = EventFactory()
        user = UserFactory()

        def quit():
            event.quit(user)
        self.assertRaises(AttributeError, quit)