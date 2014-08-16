# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings
from appconf import AppConf


class GoogleCalendarAppConf(AppConf):
    """Google Calendar configures"""

    # A target event model
    EVENT_MODEL = None

    # A backend class
    BACKEND_CLASS = None

    # Credentials (file)
    CREDENTIALS = None

    # CLIENT_SECRETS (file)
    CLIENT_SECRETS = None

    class Meta:
        prefix = 'google_calendar'
