# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from activities.notifiers.oauth.twitter import TwitterActivityNotifier


OAUTH_NOTIFIERS = {
    'twitter': TwitterActivityNotifier,
}

def _get_or_request(name, options):
    value = options.get(name)
    if not value:
        print("No {} is specified.".format(name))
        value = input("Please enter your {}".format(name))
        if not value:
            raise CommandError("Operation has canceled by user")
    return value

class Command(BaseCommand):
    args = 'service_name'
    help = (
        "Command to help for creating an OAuth credentials file."
    )

    option_list = BaseCommand.option_list + (
        make_option('-c', '--client-key'),
        make_option('-s', '--client-secret'),
        make_option('-f', '--filename', default='credentials.json'),
    )

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity'))

        if len(args) == 0:
            raise CommandError(
                "This command required at least one argument. "
                "Run the command with -h to see the help."
            )
        service_name = args[0]

        # validate preset name
        if service_name not in OAUTH_NOTIFIERS.keys():
            raise CommandError((
                "The service name '{}' is not supported."
            ).format(service_name))

        filename = options.get('filename')
        client_key = _get_or_request('client_key', options)
        client_secret = _get_or_request('client_secret', options)

        notifier_cls = OAUTH_NOTIFIERS.get(service_name)
        notifier_cls.create_credentials(filename, client_key, client_secret)

        if verbosity > 0:
            print("*" * 80)
            print()
            print("The credentials are saved in '{}'.".format(filename))
            print()
            print("*" * 80)
