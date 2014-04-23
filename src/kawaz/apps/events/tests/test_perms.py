import datetime
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.tests.datetime import patch_datetime_now
from ..models import Event
from .factories import EventFactory

from .utils import static_now
from .utils import event_factory_with_relative


@patch_datetime_now(static_now)
class EventPermissionLogicTestCase(TestCase):
    def setUp(self):
        self.users = dict(
                adam=PersonaFactory(role='adam'),
                seele=PersonaFactory(role='seele'),
                nerv=PersonaFactory(role='nerv'),
                children=PersonaFactory(role='children'),
                wille=PersonaFactory(role='wille'),
                organizer=PersonaFactory(role='children'),
                attendee=PersonaFactory(role='children'),
                anonymous=AnonymousUser(),
            )
        self.event = EventFactory(organizer=self.users['organizer'])
        self.event.attendees.add(self.users['attendee'])
        self.event.save()

    def _test_permission(self, role, perm, obj=None, negative=False):
        user = self.users.get(role)
        perm = "events.{}_event".format(perm)
        if obj:
            obj = self.event
        if negative:
            self.assertFalse(user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(user.has_perm(perm, obj=obj),
                "{} should have '{}'".format(role.capitalize(), perm))

    def test_add_permission(self):
        """
        Authenticated users except wille should have an add permission
        """
        self._test_permission('adam', 'add')
        self._test_permission('seele', 'add')
        self._test_permission('nerv', 'add')
        self._test_permission('children', 'add')
        self._test_permission('wille', 'add', negative=True)
        self._test_permission('anonymous', 'add', negative=True)

    def test_change_permission_without_obj(self):
        """
        Authenticated users except wille should have a change permission
        generally
        """
        self._test_permission('adam', 'change')
        self._test_permission('seele', 'change')
        self._test_permission('nerv', 'change')
        self._test_permission('children', 'change')
        self._test_permission('wille', 'change', negative=True)
        self._test_permission('anonymous', 'change', negative=True)

    def test_change_permission_with_obj(self):
        """
        Nobody except the organizer and adam should have a change permission of
        the particular event instance
        """
        self._test_permission('adam', 'change', obj=True)
        self._test_permission('seele', 'change', obj=True, negative=True)
        self._test_permission('nerv', 'change', obj=True, negative=True)
        self._test_permission('children', 'change', obj=True, negative=True)
        self._test_permission('wille', 'change', obj=True, negative=True)
        self._test_permission('anonymous', 'change', obj=True, negative=True)
        self._test_permission('organizer', 'change', obj=True)

    def test_delete_permission_without_obj(self):
        """
        Authenticated users except wille should have a delete permission
        generally
        """
        self._test_permission('adam', 'delete')
        self._test_permission('seele', 'delete')
        self._test_permission('nerv', 'delete')
        self._test_permission('children', 'delete')
        self._test_permission('wille', 'delete', negative=True)
        self._test_permission('anonymous', 'delete', negative=True)

    def test_delete_permission_with_obj(self):
        """
        Nobody except the organizer and adam should have a delete permission of
        the particular event instance
        """
        self._test_permission('adam', 'delete', obj=True)
        self._test_permission('seele', 'delete', obj=True, negative=True)
        self._test_permission('nerv', 'delete', obj=True, negative=True)
        self._test_permission('children', 'delete', obj=True, negative=True)
        self._test_permission('wille', 'delete', obj=True, negative=True)
        self._test_permission('anonymous', 'delete', obj=True, negative=True)
        self._test_permission('organizer', 'delete', obj=True)

    def test_attend_permission_without_obj(self):
        """
        Authenticated users should have an attend permission generally
        """
        self._test_permission('adam', 'attend')
        self._test_permission('seele', 'attend')
        self._test_permission('nerv', 'attend')
        self._test_permission('children', 'attend')
        self._test_permission('wille', 'attend')
        self._test_permission('anonymous', 'attend', negative=True)

    def test_attend_permission_with_obj(self):
        """
        Authenticated users except the organizer and the attendees
        should have an attend permission of the particular event instance
        """
        self._test_permission('adam', 'attend', obj=True)
        self._test_permission('seele', 'attend', obj=True)
        self._test_permission('nerv', 'attend', obj=True)
        self._test_permission('children', 'attend', obj=True)
        self._test_permission('wille', 'attend', obj=True)
        self._test_permission('anonymous', 'attend', obj=True, negative=True)
        self._test_permission('organizer', 'attend', obj=True, negative=True)
        self._test_permission('attendee', 'attend', obj=True, negative=True)

    def test_quit_permission_without_obj(self):
        """
        Authenticated users should have a quit permission generally
        """
        self._test_permission('adam', 'quit')
        self._test_permission('seele', 'quit')
        self._test_permission('nerv', 'quit')
        self._test_permission('children', 'quit')
        self._test_permission('wille', 'quit')
        self._test_permission('anonymous', 'quit', negative=True)

    def test_quit_permission_with_obj(self):
        """
        Attendees except the organizer should have a quit permission of
        the particular event instance
        """
        self._test_permission('adam', 'quit', obj=True)
        self._test_permission('seele', 'quit', obj=True, negative=True)
        self._test_permission('nerv', 'quit', obj=True, negative=True)
        self._test_permission('children', 'quit', obj=True, negative=True)
        self._test_permission('wille', 'quit', obj=True, negative=True)
        self._test_permission('anonymous', 'quit', obj=True, negative=True)
        self._test_permission('organizer', 'quit', obj=True, negative=True)
        self._test_permission('attendee', 'quit', obj=True)

