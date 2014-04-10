# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser

class Skill(models.Model):
    """It is the model which indicates what users can"""
    label = models.CharField(_("Label"), unique=True, max_length=32)
    order = models.IntegerField(_("Order"), default=0)

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ('order',)
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")