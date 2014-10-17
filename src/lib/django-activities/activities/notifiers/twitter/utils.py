# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import json
from django.core.exceptions import ImproperlyConfigured
from .conf import settings


def get_client_secrets(filename=None):
    """
    Get client secrets (consumer_key and consumer_secret) from a specified
    file. If no file is specified, the file specified as
    'settings.ACTIVITIES_NOTIFIERS_TWITTER_CLIENT_SECRETS' will be used.
    The return value is a dictionary which can be used as a keyword arguments
    of requests_oauthlib
    """
    if filename is None:
        filename = settings.ACTIVITIES_NOTIFIERS_TWITTER_CLIENT_SECRETS
    if filename is None:
        raise ImproperlyConfigured(
            "'ACTIVITIES_NOTIFIERS_TWITTER_CLIENT_SECRETS' is not configured "
            "in 'django.conf.settings' module. "
            "You have to configure this value to use twitter notification "
            "feature on activities app."
        )
    if not os.path.exists(filename):
        raise ImproperlyConfigured(
            "'{}' is not found. Confirm the file exists.".format(filename)
        )
    with open(filename) as fi:
        client_secrets = json.load(fi)
    # validate json
    requireds = ('consumer_key', 'consumer_secret')
    for required in requireds:
        if required not in client_secrets:
            raise ImproperlyConfigured(
                "'{}' attribute is not found in '{}'. ".format(
                    required, filename,
                )
            )
    # rename attribute to fit on requests_oauthlib
    return dict(
        client_key=client_secrets.get('consumer_key'),
        client_secret=client_secrets.get('consumer_secret'),
    )


def get_credentials(filename=None):
    """
    Get credentials (consumer_key, consumer_secret, access_token,
    access_token_secret) from a specified file. If no file is specified, the
    file specified as
    'settings.ACTIVITIES_NOTIFIERS_TWITTER_CREDENTIALS' will be used.
    The return value is a dictionary which can be used as a keyword arguments
    of requests_oauthlib
    """
    if filename is None:
        filename = settings.ACTIVITIES_NOTIFIERS_TWITTER_CREDENTIALS
    if filename is None:
        raise ImproperlyConfigured(
            "'ACTIVITIES_NOTIFIERS_TWITTER_CREDENTIALS' is not configured "
            "in 'django.conf.settings' module. "
            "You have to configure this value to use twitter notification "
            "feature on activities app."
        )
    if not os.path.exists(filename):
        raise ImproperlyConfigured(
            "'{}' is not found. Confirm the file exists.".format(filename)
        )
    with open(filename) as fi:
        credentials = json.load(fi)
    # validate json
    requireds = (
        'consumer_key', 'consumer_secret',
        'access_token', 'access_token_secret',
    )
    for required in requireds:
        if required not in credentials:
            raise ImproperlyConfigured(
                "'{}' attribute is not found in '{}'. ".format(
                    required, filename,
                )
            )
    # rename attribute to fit on requests_oauthlib
    return dict(
        client_key=credentials.get('consume_key'),
        client_secret=credentials.get('consume_secret'),
        resource_owner_key=credentials.get('access_token'),
        resource_owner_secret=credentials.get('access_token_secret'),
    )
