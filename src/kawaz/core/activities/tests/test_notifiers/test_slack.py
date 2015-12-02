import random
import string
import json
import urllib
from unittest.mock import MagicMock
from django.test import override_settings
from django.test import TestCase
from kawaz.core.activities.notifiers import slack
from kawaz.core.activities.notifiers.slack import SlackAcitivityNotifier


@override_settings(ACTIVITIES_ENABLE_SLACK_NOTIFICATION=True)
class SlackActivityNotifierTestCase(TestCase):
    def test_send(self):
        """
        SlackActivityNotifierで正しいクエリーが正しいURLにPOSTされるかをテストします
        """
        randomstr = "".join([random.choice(string.ascii_letters)
                             for x in range(100)])
        endpoint_url = 'https://kawaz.slack.com/dummyauthtoken'
        channel = '#notification'
        username = 'かわずたん'
        icon_emoji = ':frog:'
        icon_url = 'http://example.kawaz.org/kawaz.jpg'

        def dummy_request(url, data):
            self.assertEqual(url, endpoint_url)
            query = urllib.parse.parse_qs(data.decode('utf-8'))
            payload = json.loads(query['payload'][0])
            self.assertEqual(url, endpoint_url)
            self.assertEqual(payload['channel'], channel)
            self.assertEqual(payload['icon_emoji'], icon_emoji)
            self.assertEqual(payload['icon_url'], icon_url)
            self.assertEqual(payload['username'], username)
            self.assertEqual(payload['text'], randomstr)

        slack.urllib.request.Request = dummy_request
        slack.urllib.request.urlopen = MagicMock(return_value=None)

        options = {
            'username': username,
            'icon_emoji': icon_emoji,
            'icon_url': icon_url
        }
        notifier = SlackAcitivityNotifier(endpoint_url, channel, options)
        notifier.send(randomstr)
