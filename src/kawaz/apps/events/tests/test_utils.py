# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/30
#
__author__ = 'giginet'

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import EventFactory
from ..utils.gcal import GoogleCalendarUpdater

@override_settings(GOOGLE_CALENDAR_ID='hoge')
class GoogleCalendarUploaderTestCase(TestCase):
    def test_body_from_event(self):
        """
        Eventから正しい辞書を取り出せる
        """
        now = timezone.now()
        period_start = now + timezone.timedelta(3)
        period_end = now + timezone.timedelta(4)
        e = EventFactory(title="geekdrums爆発しろ会",
                         body="爆発させます",
                         period_start=period_start,
                         period_end=period_end,
                         place='安息の地'
        )
        updater = GoogleCalendarUpdater()
        body = updater.body_from_event(e)
        self.assertEqual(body['summary'], e.title)
        self.assertEqual(body['description'], e.body)
        self.assertEqual(body['start']['dateTime'], e.period_start.strftime('%Y-%m-%dT%H:%M:%S.000%z'))
        self.assertEqual(body['end']['dateTime'], e.period_end.strftime('%Y-%m-%dT%H:%M:%S.000%z'))
        self.assertEqual(body['location'], e.place)
        self.assertEqual(body['visibility'], 'public')
        self.assertEqual(len(body['attendees']), 1)
        self.assertEqual(body['attendees'][0]['displayName'], e.organizer.nickname)
        self.assertEqual(body['attendees'][0]['email'], e.organizer.email)
        self.assertEqual(body['source']['url'], '{}{}'.format('http://example.com', e.get_absolute_url()))


    def test_body_from_event_private(self):
        """
         ProtectedなEventはVisibilityがprivateになる
        """
        e = EventFactory(pub_state='protected')
        updater = GoogleCalendarUpdater()
        body = updater.body_from_event(e)
        self.assertEqual(body['visibility'], 'private')


    def test_body_from_event_attendee(self):
        """
        参加者が増えたら、attendeeの値も更新される
        """
        e = EventFactory()
        updater = GoogleCalendarUpdater()
        user0 = PersonaFactory()
        user1 = PersonaFactory()
        e.attend(user0)
        e.attend(user1)
        body = updater.body_from_event(e)

        self.assertEqual(len(body['attendees']), 3)
        self.assertEqual(body['attendees'][0]['displayName'], e.organizer.nickname)
        self.assertEqual(body['attendees'][0]['email'], e.organizer.email)
        self.assertEqual(body['attendees'][1]['displayName'], user0.nickname)
        self.assertEqual(body['attendees'][1]['email'], user0.email)
        self.assertEqual(body['attendees'][2]['displayName'], user1.nickname)
        self.assertEqual(body['attendees'][2]['email'], user1.email)

