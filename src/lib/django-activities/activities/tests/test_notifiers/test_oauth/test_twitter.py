# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import json
import random
from unittest import skipUnless
from django.test import TestCase
from django.test.utils import override_settings
from ....notifiers.oauth.twitter import TwitterActivityNotifier


TEST_CREDENTIALS = os.path.join(
    os.path.dirname(__file__), 'data', 'credentials_twitter.json'
)


@skipUnless(
    os.path.exists(TEST_CREDENTIALS),
    "A credentials file '{}' is not found.".format(TEST_CREDENTIALS)
)
class TwitterActivityNotifierTestCase(TestCase):
    @override_settings(
        ACTIVITIES_ENABLE_OAUTH_NOTIFICATION=True,
    )
    def test_send(self):
        credentials = TwitterActivityNotifier.get_credentials(
            TEST_CREDENTIALS
        )
        randomstr = "".join([random.choice("abcdefghijklmnopqrstuvwxyz")
                             for x in range(100)])
        randomstr = "django-activities: {}".format(randomstr)
        notifier = TwitterActivityNotifier(credentials)
        notifier.send(randomstr)

        # get screen name
        url = 'https://api.twitter.com/1.1/account/settings.json'
        response = notifier.oauth_session.get(url)
        info = json.loads(response.text)
        screen_name = info['screen_name']
        # get latest tweet
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        response = notifier.oauth_session.get(url, params=dict(
            screen_name=screen_name,
            count=1,
        ))
        tweet = json.loads(response.text)
        self.assertEqual(tweet[0]['text'], randomstr)
