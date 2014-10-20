from datetime import timedelta
from unittest.mock import MagicMock
from django.test import TestCase
from django.utils import timezone
from activities.models import Activity
from .factories import EventFactory, PersonaFactory
from ..models import Event
from ..activity import EventActivityMediator


class EventActivityMediatorTestCase(TestCase):

    def test_create_event(self):
        nactivity = Activity.objects.get_for_model(Event).count()

        event = EventFactory()
        self.assertEqual(nactivity+1,
                         Activity.objects.get_for_model(Event).count())
        activity = Activity.objects.get_for_model(Event).first()
        self.assertEqual(activity.snapshot, event)
        self.assertEqual(activity.status, 'created')

    def test_update_event(self):
        event = EventFactory()

        nactivity = Activity.objects.get_for_model(Event).count()
        event.period_start = event.period_start + timedelta(hours=2)
        event.period_end = event.period_end + timedelta(hours=2)
        event.attendance_deadline = timezone.now() + timedelta(minutes=30)
        event.save()

        self.assertEqual(nactivity+1,
                         Activity.objects.get_for_model(Event).count())
        activity = Activity.objects.get_for_model(Event).first()
        self.assertEqual(activity.snapshot, event)
        self.assertEqual(activity.status, 'updated')
        self.assertTrue('period_start_updated' in activity.remarks)
        self.assertTrue('period_end_updated' in activity.remarks)
        self.assertTrue('attendance_deadline_created' in activity.remarks)

    def test_delete_event(self):
        event = EventFactory()

        nactivity = Activity.objects.get_for_model(Event).count()
        pk = event.pk       # delete() により消去される pk を保持
        event.delete()
        event.pk = pk       # snapshotと比較するためpkを最適用（存在しない）
        self.assertEqual(nactivity+1,
                         Activity.objects.get_for_model(Event).count())
        activity = Activity.objects.get_for_model(Event).first()
        self.assertEqual(activity.snapshot, event)
        self.assertEqual(activity.status, 'deleted')

    def test_attend_event(self):
        event = EventFactory()
        user1 = PersonaFactory()
        user2 = PersonaFactory()

        nactivity = Activity.objects.get_for_model(Event).count()

        event.attend(user1)
        self.assertEqual(nactivity+1,
                         Activity.objects.get_for_model(Event).count())
        activity = Activity.objects.get_for_model(Event).first()
        self.assertEqual(activity.snapshot, event)
        self.assertEqual(activity.status, 'user_add')
        self.assertTrue(str(user1.pk) in activity.remarks)

        event.attend(user2)
        self.assertEqual(nactivity+2,
                         Activity.objects.get_for_model(Event).count())
        activity = Activity.objects.get_for_model(Event).first()
        self.assertEqual(activity.snapshot, event)
        self.assertEqual(activity.status, 'user_add')
        self.assertTrue(str(user2.pk) in activity.remarks)

    def test_quit_event(self):
        event = EventFactory()
        user1 = PersonaFactory()
        user2 = PersonaFactory()
        event.attend(user1)
        event.attend(user2)

        nactivity = Activity.objects.get_for_model(Event).count()

        event.quit(user1)
        self.assertEqual(nactivity+1,
                         Activity.objects.get_for_model(Event).count())
        activity = Activity.objects.get_for_model(Event).first()
        self.assertEqual(activity.snapshot, event)
        self.assertEqual(activity.status, 'user_removed')
        self.assertTrue(str(user1.pk) in activity.remarks)

        event.quit(user2)
        self.assertEqual(nactivity+2,
                         Activity.objects.get_for_model(Event).count())
        activity = Activity.objects.get_for_model(Event).first()
        self.assertEqual(activity.snapshot, event)
        self.assertEqual(activity.status, 'user_removed')
        self.assertTrue(str(user2.pk) in activity.remarks)
