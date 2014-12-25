# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models

APP_LABEL = 'historywall'


class HistoryWallTestModelA(models.Model):
    text = models.CharField('text', max_length=30)

    class Meta:
        app_label = APP_LABEL


class HistoryWallTestModelB(models.Model):
    text = models.CharField('text', max_length=30)

    class Meta:
        app_label = APP_LABEL


class HistoryWallTestModelC(models.Model):
    text = models.CharField('text', max_length=30)

    class Meta:
        app_label = APP_LABEL
