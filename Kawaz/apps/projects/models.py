from django.db import models
from django.utils.translation import ugettext as _

class Category(models.Model):
    """
    This model indicates category of each projects
    """
    label = models.CharField(_('Name'), max_length=32, unique=True)
    parent = models.ForeignKey('self', verbose_name=_('Parent category'), null=True, blank=True, related_name='children')

    class Meta:
        ordering = ('label',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categorys')

    def __str__(self):
        return self.label
