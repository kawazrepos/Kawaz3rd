# coding=utf-8
"""
"""

from django.conf import settings
from appconf import AppConf


class ActivitiesHatenablogAppConf(AppConf):
    FEED_URL = ''

    class Meta:
        prefix = 'activities_hatenablog'

