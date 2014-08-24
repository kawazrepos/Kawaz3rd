import os
from django.conf import settings
from django.core.management.base import BaseCommand
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


class Command(BaseCommand):
    """
    Login to Google Calendar API to obtain the credentials

    Usage:
        python manage.py login_to_google_calendar_api
    """
    def handle(self, *args, **options):
        print("=" * 50)
        print(" Login to Google Calendar API")
        print("=" * 50)
        flow = flow_from_clientsecrets(
            settings.GCAL_CLIENT_SECRETS,
            scope='https://www.googleapis.com/auth/calendar',
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')

        auth_uri = flow.step1_get_authorize_url()

        print("Open the following URL to authorize the API")
        print()
        print(auth_uri)
        print()
        code = input("Please fill the code: ")

        if not code:
            print("Canceled")
            exit(1)

        credentials = flow.step2_exchange(code)

        storage = Storage(settings.GCAL_CREDENTIALS)
        storage.put(credentials)

        print("Credentials are saved in '{}'".format(
            settings.GCAL_CREDENTIALS))
