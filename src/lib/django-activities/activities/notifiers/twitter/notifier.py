# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import json
from requests_oauthlib import OAuth1Session
from .conf import settings
from .utils import get_credentials
from activities.notifiers.base import ActivityNotifier


class ActivityTwitterNotifier(ActivityNotifier):
    typename = 'twitter'

    def send(self, rendered):
        credentials = get_credentials()
        session = OAuth1Session(**credentials)
        params = dict(
            status=rendered,
        )
        res = session.post(
            'https://api.twitter.com/1.1/statuses/update.json',
            params=params,
        )
