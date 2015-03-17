import random
import string
import urllib
from unittest.mock import MagicMock
from django.test import override_settings
from django.test import TestCase
from kawaz.core.activities.notifiers import hipchat
from kawaz.core.activities.notifiers.hipchat import HipChatActivityNotifier

__author__ = 'giginet'

class HipChatActivityNotifierTestCase(TestCase):
    @override_settings(ACTIVITIES_ENABLE_HIPCHAT_NOTIFICATION=True)
    def test_send(self):
        """
        HipChatActivityNotifierで正しいクエリーが正しいURLにPOSTされるかをテストします
        """
        randomstr = "".join([random.choice(string.ascii_letters)
                             for _ in range(100)])
        auth_token = 'dummyauthtoken'
        room_id = '9999999'

        def dummy_request(url, data):
            self.assertEqual(url, 'https://api.hipchat.com/v1/rooms/message')
            data = data.decode('utf-8')
            query = urllib.parse.parse_qs(data)
            self.assertEqual(query['auth_token'][0], auth_token)
            self.assertEqual(query['room_id'][0], room_id)
            self.assertEqual(query['color'][0], 'random')
            self.assertEqual(query['notify'][0], 'True')
            self.assertEqual(query['from'][0], 'Kawaz')
            self.assertEqual(query['message'][0], randomstr)

        hipchat.urllib.request.Request = dummy_request
        hipchat.urllib.request.urlopen = MagicMock(return_value=None)

        notifier = HipChatActivityNotifier(auth_token, room_id)
        notifier.send(randomstr)