# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import json
from requests_oauthlib import OAuth1Session
from django.core.exceptions import ImproperlyConfigured
from ..base import ActivityNotifierBase


class OAuth1ActivityNotifier(ActivityNotifierBase):
    """
    An activity notifer class which use POST to send rendered content but
    OAuth1 authorization is required.
    """
    # used to send a notification
    url = None
    key = 'data'
    params = {}

    # used to create a credentials
    request_token_url=None
    authorization_base_url=None
    access_token_url=None

    def __init__(self, credentials, params={}):
        params = dict(params)
        params.update(credentials)
        self.oauth_session = OAuth1Session(**params)

    def send(self, rendered_content):
        params = dict(self.params)
        params[self.key] = rendered_content
        self.oauth_session.post(self.url, data=params)

    @classmethod
    def get_credentials(cls, filename):
        """
        Get credentials (client_key, client_secret, resource_owner_key,
        resource_owner_secret) from a specified file.
        The return value is a dictionary to initialize a
        requests_oauthlib.OAuth1
        """
        if not os.path.exists(filename):
            raise ImproperlyConfigured((
                "'{}' is not found. Confirm if the file exists."
            ).format(filename))
        with open(filename) as fi:
            credentials = json.load(fi)
        # validate json
        requireds = (
            'client_key', 'client_secret',
            'resource_owner_key', 'resource_owner_secret',
        )
        for required in requireds:
            if required not in credentials:
                raise ImproperlyConfigured(
                    "'{}' attribute is not found in '{}'. ".format(
                        required, filename,
                    )
                )
        return credentials

    @classmethod
    def create_credentials(cls, filename, client_key, client_secret, **params):
        session = OAuth1Session(client_key, client_secret, **params)
        session.fetch_request_token(cls.request_token_url)
        authorization_url = session.authorization_url(
            cls.authorization_base_url
        )
        print(
            "Please open the following url and input the PIN CODE "
            "showed in that web page."
        )
        print()
        print(authorization_url)
        print()
        pin = input("PIN CODE: ")
        access_tokens = session.fetch_access_token(
            cls.access_token_url, verifier=pin
        )
        resource_owner_key = access_tokens.get('oauth_token')
        resource_owner_secret = access_tokens.get('oauth_token_secret')

        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as fo:
            json.dump(dict(
                client_key=client_key,
                client_secret=client_secret,
                resource_owner_key=resource_owner_key,
                resource_owner_secret=resource_owner_secret,
            ), fo)
