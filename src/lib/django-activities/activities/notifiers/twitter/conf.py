# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings
from appconf import AppConf


class ActivitiesNotifiersTwitterAppConf(AppConf):
    CLIENT_SECRETS = None
    CREDENTIALS = None

    class Meta:
        prefix = 'activities_notifiers_twitter'
