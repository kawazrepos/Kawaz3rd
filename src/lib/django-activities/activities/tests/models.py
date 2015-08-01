# coding=utf-8
"""
"""

from django.db import models
from kawaz.core.personas.models import Persona
from kawaz.core.publishments.models import PUB_STATES


class ActivitiesTestModelA(models.Model):
    text = models.CharField('text', max_length=30)
    class Meta:
        app_label = 'activities'

class ActivitiesTestModelB(models.Model):
    text = models.CharField('text', max_length=30)
    class Meta:
        app_label = 'activities'

class ActivitiesTestModelC(models.Model):
    text = models.CharField('text', max_length=30)
    class Meta:
        app_label = 'activities'
