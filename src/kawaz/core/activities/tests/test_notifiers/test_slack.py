import random
import string
import json
import urllib
from unittest.mock import patch
from django.test import override_settings
from django.test import TestCase
from kawaz.core.activities.notifiers.slack import SlackActivityNotifier


@override_settings(ACTIVITIES_ENABLE_SLACK_NOTIFICATION=True)
class SlackActivityNotifierTestCase(TestCase):
    def setUp(self):
        self.randomstr = "".join([random.choice(string.ascii_letters)
                                  for _ in range(100)])

    def assert_send(self, rendered_str, message, username='かわずたん', icon_url='http://dummy.kawaz.com/'):
        endpoint_url = 'https://kawaz.slack.com/dummyauthtoken'
        channel = '#notification'
        icon_emoji = ':frog:'

        def dummy_request(url, data):
            self.assertEqual(url, endpoint_url)
            query = urllib.parse.parse_qs(data.decode('utf-8'))
            payload = json.loads(query['payload'][0])
            self.assertEqual(url, endpoint_url)
            self.assertEqual(payload['channel'], channel)
            self.assertEqual(payload['icon_emoji'], icon_emoji)
            self.assertEqual(payload['icon_url'], icon_url)
            self.assertEqual(payload['username'], username)
            self.assertEqual(payload['text'], message)

        with patch('urllib.request') as request:
            request.Request = dummy_request
            request.urlopen.return_value = None

            options = {
                'username': username,
                'icon_emoji': icon_emoji,
                'icon_url': icon_url
            }
            notifier = SlackActivityNotifier(endpoint_url, channel, options)
            notifier.send(rendered_str)

    def test_send(self):
        """
        SlackActivityNotifierで正しいクエリーが正しいURLにPOSTされる
        """
        self.assertEqual(self.randomstr, self.randomstr)

    def test_send_with_username_tag(self):
        """
        usernameタグが冒頭に含まれてたとき、ユーザー名が変わる
        """
        message = '\n'.join(('<username=井の中かわず>', self.randomstr))
        self.assertEqual(self.assert_send(message, self.randomstr, username='井の中かわず'))

    def test_send_with_icon_url_tag(self):
        """
        icon_urlタグが冒頭に含まれてたとき、アイコンが変わる
        """
        message = '\n'.join(('<icon_url=http://example.kawaz.org/icon.jpg>', self.randomstr))
        self.assertEqual(self.assert_send(message, self.randomstr, icon_url='http://example.kawaz.org/icon.jpg'))

    def test_send_with_invalid_tag(self):
        """
        無効なタグが冒頭に含まれてたとき無視する
        """
        message = '\n'.join(('<invalid_key=invalid_key>', self.randomstr))
        self.assertEqual(self.assert_send(message, self.randomstr))

    def test_send_with_username_and_icon_url_tags(self):
        """
        正しいタグが冒頭に複数個含まれてたとき、ユーザー名とアイコンが変わる
        """
        message = '\n'.join(('<username=井の中かわず>', '<icon_url=http://example.kawaz.org/icon.jpg>', self.randomstr))
        self.assertEqual(self.assert_send(message, self.randomstr, '井の中かわず', 'http://example.kawaz.org/icon.jpg'))

    def test_valid_tag_with_invalid_position(self):
        """
        正しいタグが冒頭以外に含まれてたとき、無視してそのまま出力する
        """
        message = '\n'.join((self.randomstr, '<username=井の中かわず>'))
        self.assertEqual(self.assert_send(message, message))
