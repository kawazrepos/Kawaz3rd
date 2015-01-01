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
    modela = models.ForeignKey(HistoryWallTestModelA, null=True)

    class Meta:
        app_label = APP_LABEL


class HistoryWallTestModelC(models.Model):
    text = models.CharField('text', max_length=30)
    modelas = models.ManyToManyField(HistoryWallTestModelA)
    modelbs = models.ManyToManyField(HistoryWallTestModelB,
                                     related_name='modelcs')

    class Meta:
        app_label = APP_LABEL
