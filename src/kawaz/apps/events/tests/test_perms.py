import datetime
from unittest import mock
from kawaz.core.personas.models import Persona
from kawaz.core.tests.testcases.permissions import BasePermissionLogicTestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Event
from .factories import EventFactory

from .utils import static_now
from .utils import event_factory_with_relative


@mock.patch('django.utils.timezone.now', static_now)
class EventPermissionLogicTestCase(BasePermissionLogicTestCase):
    app_label = 'events'
    model_name = 'event'

    def setUp(self):
        super().setUp()
        self.users['organizer'] = PersonaFactory(username='organizer',
                                                 role='children')
        self.users['attendee'] = PersonaFactory(username='attendee',
                                                role='children')
        self.event = EventFactory(organizer=self.users['organizer'])
        self.event.attendees.add(self.users['attendee'])
        self.event.save()

        self.event_over_restriction = EventFactory(number_restriction=1)
        static_now_past = lambda: static_now() - datetime.timedelta(hours=48)
        attendance_deadline = static_now() - datetime.timedelta(hours=24)
        with mock.patch('django.utils.timezone.now', static_now_past):
            self.event_over_deadline = EventFactory(
                    attendance_deadline=attendance_deadline)

    def test_add_permission(self):
        """
        Authenticated users except wille should have an add permission
        """
        self._test('adam', 'add')
        self._test('seele', 'add')
        self._test('nerv', 'add')
        self._test('children', 'add')
        self._test('wille', 'add', neg=True)
        self._test('anonymous', 'add', neg=True)

    def test_change_permission_without_obj(self):
        """
        Authenticated users except wille should have a change permission
        generally
        """
        self._test('adam', 'change')
        self._test('seele', 'change')
        self._test('nerv', 'change')
        self._test('children', 'change')
        self._test('wille', 'change', neg=True)
        self._test('anonymous', 'change', neg=True)

    def test_change_permission_with_obj(self):
        """
        Nobody except the organizer and adam should have a change permission of
        the particular event instance
        """
        self._test('adam', 'change', obj=self.event)
        self._test('seele', 'change', obj=self.event, neg=True)
        self._test('nerv', 'change', obj=self.event, neg=True)
        self._test('children', 'change', obj=self.event, neg=True)
        self._test('wille', 'change', obj=self.event, neg=True)
        self._test('anonymous', 'change', obj=self.event, neg=True)
        self._test('organizer', 'change', obj=self.event)
        self._test('attendee', 'change', obj=self.event)

    def test_delete_permission_without_obj(self):
        """
        Authenticated users except wille should have a delete permission
        generally
        """
        self._test('adam', 'delete')
        self._test('seele', 'delete')
        self._test('nerv', 'delete')
        self._test('children', 'delete')
        self._test('wille', 'delete', neg=True)
        self._test('anonymous', 'delete', neg=True)

    def test_delete_permission_with_obj(self):
        """
        Nobody except the organizer and adam should have a delete permission of
        the particular event instance
        """
        self._test('adam', 'delete', obj=self.event)
        self._test('seele', 'delete', obj=self.event, neg=True)
        self._test('nerv', 'delete', obj=self.event, neg=True)
        self._test('children', 'delete', obj=self.event, neg=True)
        self._test('wille', 'delete', obj=self.event, neg=True)
        self._test('anonymous', 'delete', obj=self.event, neg=True)
        self._test('organizer', 'delete', obj=self.event)

    def test_attend_permission_without_obj(self):
        """
        Authenticated users should have an attend permission generally
        """
        self._test('adam', 'attend')
        self._test('seele', 'attend')
        self._test('nerv', 'attend')
        self._test('children', 'attend')
        self._test('wille', 'attend')
        self._test('anonymous', 'attend', neg=True)

    def test_attend_permission_with_obj(self):
        """
        Authenticated users except the organizer and the attendees
        should have an attend permission of the particular event instance
        """
        self._test('adam', 'attend', obj=self.event)
        self._test('seele', 'attend', obj=self.event)
        self._test('nerv', 'attend', obj=self.event)
        self._test('children', 'attend', obj=self.event)
        self._test('wille', 'attend', obj=self.event)
        self._test('anonymous', 'attend', obj=self.event, neg=True)

        # django-permissionのキャッシュ対応
        organizer = Persona.objects.get(pk=self.users['organizer'].pk)
        self.users['organizer'] = organizer

        self._test('organizer', 'attend', obj=self.event, neg=True)
        self._test('attendee', 'attend', obj=self.event, neg=True)

    def test_attend_permission_with_obj_over_restriction(self):
        """
        人数制限を超えているイベントには参加不可
        """
        event = self.event_over_restriction
        self._test('adam', 'attend', obj=event)
        self._test('seele', 'attend', obj=event, neg=True)
        self._test('nerv', 'attend', obj=event, neg=True)
        self._test('children', 'attend', obj=event, neg=True)
        self._test('wille', 'attend', obj=event, neg=True)
        self._test('anonymous', 'attend', obj=event, neg=True)
        self._test('organizer', 'attend', obj=event, neg=True)
        self._test('attendee', 'attend', obj=event, neg=True)

    def test_attend_permission_with_obj_over_deadline(self):
        """
        参加締め切りを過ぎたイベントには参加不可
        """
        event = self.event_over_deadline
        self._test('adam', 'attend', obj=event)
        self._test('seele', 'attend', obj=event, neg=True)
        self._test('nerv', 'attend', obj=event, neg=True)
        self._test('children', 'attend', obj=event, neg=True)
        self._test('wille', 'attend', obj=event, neg=True)
        self._test('anonymous', 'attend', obj=event, neg=True)
        self._test('organizer', 'attend', obj=event, neg=True)
        self._test('attendee', 'attend', obj=event, neg=True)

    def test_quit_permission_without_obj(self):
        """
        Authenticated users should have a quit permission generally
        """
        self._test('adam', 'quit')
        self._test('seele', 'quit')
        self._test('nerv', 'quit')
        self._test('children', 'quit')
        self._test('wille', 'quit')
        self._test('anonymous', 'quit', neg=True)

    def test_quit_permission_with_obj(self):
        """
        Attendees except the organizer should have a quit permission of
        the particular event instance
        """
        self._test('adam', 'quit', obj=self.event)
        self._test('seele', 'quit', obj=self.event, neg=True)
        self._test('nerv', 'quit', obj=self.event, neg=True)
        self._test('children', 'quit', obj=self.event, neg=True)
        self._test('wille', 'quit', obj=self.event, neg=True)
        self._test('anonymous', 'quit', obj=self.event, neg=True)
        self._test('organizer', 'quit', obj=self.event, neg=True)
        self._test('attendee', 'quit', obj=self.event)

