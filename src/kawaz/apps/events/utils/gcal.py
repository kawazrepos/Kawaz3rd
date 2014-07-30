# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/28
#
__author__ = 'giginet'
import httplib2
from rauth import OAuth2Service
from django.conf import settings
import argparse
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPE = ['https://www.googleapis.com/auth/calendar']
USER_AGENT = 'Kawaz3rd'

def _login_to():
    pass

def update_gcal(sender, instance, created, **kwargs):
    service = _login_to()
    response = service.calendars().get(calendarId='primary').execute()
    print(response)

update_gcal(None, None, None)