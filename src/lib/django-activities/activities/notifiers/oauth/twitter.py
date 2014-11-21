# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from .base import OAuth1ActivityNotifier


class TwitterActivityNotifier(OAuth1ActivityNotifier):
    typename = 'twitter'

    url = 'https://api.twitter.com/1.1/statuses/update.json'
    key = 'status'

    request_token_url='https://api.twitter.com/oauth/request_token'
    authorization_base_url='https://api.twitter.com/oauth/authorize'
    access_token_url='https://api.twitter.com/oauth/access_token'

    @classmethod
    def create_credentials(cls, filename, client_key, client_secret, **params):
        if 'callback_uri' not in params:
            params['callback_uri'] = 'oob'
        super().create_credentials(
            filename, client_key, client_secret, **params
        )

