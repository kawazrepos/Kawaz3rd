# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import sys
import json
from optparse import make_option
from django.conf import settings
from django.core.management.base import NoArgsCommand
from requests_oauthlib import OAuth1Session
from ...conf import settings
from ...utils import get_client_secrets


DEFAULT_CLIENT_SECRETS = settings.ACTIVITIES_NOTIFIERS_TWITTER_CLIENT_SECRETS
DEFAULT_CREDENTIALS = settings.ACTIVITIES_NOTIFIERS_TWITTER_CREDENTIALS

request_token_url = 'https://api.twitter.com/oauth/request_token'
authorization_url = 'https://api.twitter.com/oauth/authorize'
access_token_url = 'https://api.twitter.com/oauth/access_token'

class Command(NoArgsCommand):
    help = (
        "Command to login Twitter account for Twitter notifier of activities "
        "app via specified client_secrets.json"
    )

    option_list = NoArgsCommand.option_list + (
        make_option('-c', '--client-secrets', default=DEFAULT_CLIENT_SECRETS,
                    help=("A filename which contains client secrets")),
        make_option('-r', '--credentials', default=DEFAULT_CREDENTIALS,
                    help=("A filename which credentials will be written")),
    )

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity'))
        client_secrets = options.get('client_secrets')
        credentials = options.get('credentials')

        if os.path.exists(credentials):
            confirm = input((
                "A file '{}' exists. "
                "Do you want to overwrite it? [y/N]: "
            ).format(credentials))
        else:
            confirm = 'yes'
        if confirm not in ('y', 'yes', 'Yes', 'YES'):
            print(("Operation has canceled by user"))
            sys.exit(1)

        client_secrets = get_client_secrets(client_secrets)
        session = OAuth1Session(callback_uri='oob', **client_secrets)
        session.fetch_request_token(request_token_url)

        url = session.authorization_url(authorization_url)
        print(
            "Please open the following url and input the PIN CODE "
            "showed in that web page."
        )
        print()
        print(url)
        print()
        pin = input("PIN CODE: ")
        access_tokens = session.fetch_access_token(access_token_url,
                                                   verifier=pin)

        # create required directories
        if not os.path.exists(os.path.dirname(credentials)):
            os.makedirs(os.path.dirname(credentials))

        with open(credentials, 'w') as fo:
            json.dump(dict(
                consumer_key=client_secrets.get('consumer_key'),
                consumer_secret=client_secrets.get('consumer_secret'),
                access_token=access_tokens.get('oauth_token'),
                access_token_secret=access_tokens.get('oauth_token_secret'),
            ), fo)

        if verbosity > 0:
            print("*" * 80)
            print()
            print("Login as {}".format(access_tokens.get('screen_name')))
            print("The credentials are saved in '{}'.".format(credentials))
            print()
            print("*" * 80)

