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
from ...conf import settings


DEFAULT_CLIENT_SECRETS = settings.ACTIVITIES_NOTIFIERS_TWITTER_CLIENT_SECRETS


class Command(NoArgsCommand):
    help = (
        "Command to create client_secrets.json for Twitter notifiers of "
        "actitivies app. "
    )

    option_list = NoArgsCommand.option_list + (
        make_option('-c', '--client-secrets', default=DEFAULT_CLIENT_SECRETS,
                    help=("A filename which client secrets will be written")),
        make_option('--noinput', dest='interactive',
                    action='store_false', default=True,
                    help=("Tells Django to NOT prompt the user "
                          "for input of any kind.")),
        make_option('-k', '--consumer-key',
                    help=("A consumer key which provided in Twitter "
                          "Application Manager.")),
        make_option('-s', '--consumer-secret',
                    help=("A consumer secret which provided in Twitter "
                          "Application Manager.")),
    )

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity'))
        client_secrets = options.get('client_secrets')
        interactive = options.get('interactive')
        consumer_key = options.get('consumer_key')
        consumer_secret = options.get('consumer_secret')

        if os.path.exists(client_secrets) and interactive:
            confirm = input((
                "A file '{}' exists. "
                "Do you want to overwrite it? [y/N]: "
            ).format(client_secrets))
        else:
            confirm = 'yes'
        if confirm not in ('y', 'yes', 'Yes', 'YES'):
            print(("Operation has canceled by user"))
            sys.exit(1)

        if not consumer_key and not interactive:
            print(("'consumer_key' is not provided. Exit."))
            sys.exit(1)
        elif not consumer_key:
            consumer_key = input((
                "Please input a consumer key which is provided in "
                "Twitter Application Manager: "
            ))

        if not consumer_secret and not interactive:
            print(("'consumer_secret' is not provided. Exit."))
            sys.exit(1)
        elif not consumer_secret:
            consumer_secret = input((
                "Please input a consumer secret which is provided in "
                "Twitter Application Manager: "
            ))

        # create required directories
        if not os.path.exists(os.path.dirname(client_secrets)):
            os.makedirs(os.path.dirname(client_secrets))

        with open(client_secrets, 'w') as fo:
            json.dump(dict(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
            ), fo)

        if verbosity > 0:
            print("*" * 80)
            print()
            print("The client secrets are saved in '{}'.").format(
                client_secrets
            ))
            print()
            print("*" * 80)
