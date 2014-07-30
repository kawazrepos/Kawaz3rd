# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/30
#
__author__ = 'giginet'

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import httplib2
import argparse
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client import tools

class Command(BaseCommand):
    """
    oAuth2のアクセストークンを取得します

    Usage:
        python manage.py login_to_google
    """
    def handle(self, *args, **options):
        client_secrets = settings.GOOGLE_CLIENT_SECRET_PATH
        storage_path = settings.GOOGLE_CREDENTIALS_PATH
        scope = settings.GOOGLE_CLIENT_SCOPES

        if not os.path.exists(client_secrets):
            raise ImproperlyConfigured('{] is not exist. Please put this config.'.format(client_secrets))
        parent_parsers = [tools.argparser]
        parent_parsers.extend([])
        parser = argparse.ArgumentParser(
          description=__doc__,
          formatter_class=argparse.RawDescriptionHelpFormatter,
          parents=parent_parsers)
        flags = parser.parse_args(['--noauth_local_webserver'])

        flow = client.flow_from_clientsecrets(client_secrets, scope=scope)

        storage = file.Storage(storage_path)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            tools.run_flow(flow, storage, flags)
        else:
            print("the credential is saved already.")
            exit(0)
