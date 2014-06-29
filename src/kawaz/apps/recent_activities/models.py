import os
from django.db import models
from django.utils.translation import ugettext as _

class RecentActivity(models.Model):
    """
    最近の活動状況を表すモデルです
    主にはてなブログで運営されているKawaz広報ブログからfetchしてくる仕組みを想定しています
    """
    def _get_upload_path(self, filename):
        basedir = os.path.join('thumbnails', 'recent_activities', self.pk)
        return os.path.join(basedir, filename)

    title = models.CharField(_('Title'), max_length=128)
    url = models.URLField(_('URL'), unique=True)
    thumbnail = models.ImageField(_('Image'), upload_to=_get_upload_path)
    publish_at = models.DateTimeField(_('Created at'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish_at',)
        verbose_name = _('Recent Activity')
        verbose_name_plural = _('Recent Activities')
