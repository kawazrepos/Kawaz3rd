# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings
from appconf import AppConf


class GoogleCalendarAppConf(AppConf):
    """GoogleCalendar configures"""

    # A target event model
    EVENT_MODEL = None

    # A backend class
    BACKEND_CLASS = None

    # Google Calendar ID
    CALENDAR_ID = None

    # Google OAuth2 client secrets file (json)
    CLIENT_SECRETS = None

    # Google OAuth2 credentials file (json)
    CREDENTIALS = None
