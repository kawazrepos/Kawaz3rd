import os
import argparse
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from oauth2client import tools
from ...client import GoogleCalendarClient


class Command(BaseCommand):
    """
    Login to Google Calendar API and store an obtained credentials into a file
    storage. This command is required to be called for enabling Google Calendar
    Sync feature.

    Usage:
        python manage.py login_to_google_calendar_api
    """
    def handle(self, *args, **options):
        client_secrets = settings.GOOGLE_CALENDAR_CLIENT_SECRETS
        if not os.path.exists(client_secrets):
            raise ImproperlyConfigured(('Google Calendar API client secrets '
                                        '({}) is not found. '
                                        'Please create a correct client '
                                        'secrets json file and try again.'
                                       ).format(client_secrets))
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser],
        )
        import sys
        flags = parser.parse_args(['--noauth_local_webserver'])

        if not GoogleCalendarClient.console_login(flags):
            exit(1)
