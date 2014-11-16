# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import json
import tolerance
from requests_oauthlib import OAuth1Session
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from ..base import ActivityNotifierBase


def tolerate(fn):
    """
    A function decorator to make the function fail silently if 
    settings.DEBUG is False or fail_silently=True is specified
    """
    def switch_function(*args, **kwargs):
        fail_silently = kwargs.pop('fail_silently', True)
        if settings.DEBUG or not fail_silently:
            return False, args, kwargs
        return True, args, kwargs
    return tolerance.tolerate(switch=switch_function)(fn)


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

    @tolerate
    def send(self, rendered_content):
        if not settings.ACTIVITIES_ENABLE_OAUTH_NOTIFICATION:
            return
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
