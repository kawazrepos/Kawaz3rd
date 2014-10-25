# coding=utf-8
"""
"""
__author__ = 'giginet'
from django.db import models
from kawaz.core.personas.models import Persona
from kawaz.core.publishments.models import PUB_STATES


class KawazActivitiesTestModelA(models.Model):
    text = models.CharField('text', max_length=30)
    class Meta:
        app_label = 'activities'

class KawazActivitiesTestModelB(models.Model):
    text = models.CharField('text', max_length=30)
    class Meta:
        app_label = 'activities'

