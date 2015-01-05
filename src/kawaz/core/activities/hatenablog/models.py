import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from kawaz.core.files.storages import OverwriteStorage


class HatenablogEntry(models.Model):
    """
    はてなブログで運営されているKawaz広報ブログの各エントリーを表すモデル
    """
    def _get_upload_path(self, filename):
        basedir = os.path.join('thumbnails',
                               'activities',
                               'contrib',
                               'hatenablog')
        return os.path.join(basedir, filename)

    title = models.CharField(_('Title'), max_length=128)
    url = models.URLField(_('URL'), unique=True)
    thumbnail = models.ImageField(_('Image'),
                                  storage=OverwriteStorage(),
                                  upload_to=_get_upload_path,
                                  default='')
    md5 = models.CharField(max_length=32)
    created_at = models.DateTimeField(_('Created at'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Hatenablog entry')
        verbose_name_plural = _('Hatenablog entries')

    def get_absolute_url(self):
        return self.url

from .activity import HatenablogEntryActivityMediator
from activities.registry import registry
registry.register(HatenablogEntry,
                  HatenablogEntryActivityMediator())
