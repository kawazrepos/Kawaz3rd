import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.conf import settings

from thumbnailfield.fields import ThumbnailField

class Persona(AbstractUser):

    def _get_upload_path(self, filename):
        return os.path.join('thumbnails', 'profiles', self.user.username, filename)

    GENDER_TYPES = (
        ('man',   _("Man")),
        ('woman', _("Woman")),
        ('unknown', _("Unknown"))
    )

    nickname = models.CharField(_('Nickname'), max_length=30)
    quotes = models.CharField(_('Mood message'), max_length=127, blank=True, null=True)
    avatar = ThumbnailField(_('Avatar') , upload_to=_get_upload_path, blank=True, patterns=settings.THUMBNAIL_SIZE_PATTERNS, null=True)
    gender = models.CharField('Gender', max_length=10, choices=GENDER_TYPES, default='unknown')

    class Meta:
        ordering = ('username',)
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username
        super().save(*args, **kwargs)
