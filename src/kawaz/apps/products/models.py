import os
from django.db import models
from django.utils.translation import ugettext as _
from markupfield.fields import MarkupField
from thumbnailfield.fields import ThumbnailField

from kawaz.core.personas.models import Persona
from kawaz.apps.projects.models import Project

class Platform(models.Model):

    def _get_upload_path(self, filename):
        path = 'icons/platforms/%s' % self.label.lower()
        return os.path.join(path, filename)

    label = models.CharField(_('Label'), max_length=32)
    icon  = models.ImageField(_('Icon'), upload_to=_get_upload_path)

    class Meta:
        ordering = ('label',)
        verbose_name = _('Platform')
        verbose_name_plural = _('Platforms')

class Category(models.Model):

    label       = models.CharField(_('Label'), max_length=32, unique=True)
    description = models.CharField(_('Description'), max_length=128)

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Product(models.Model):

    def _get_upload_path(self, filename):
        path = 'products/{}/advertisement_images'.format(self.slug)
        return os.path.join(path, filename)

    DISPLAY_MODES = (
        (0, _('Carousel ')),
        (1, _('Pickup')),
        (2, _('Tiled')),
        (3, _('Text')),
    )

    title               = models.CharField(_('Title'), max_length=128, unique=True)
    slug                = models.SlugField(_('Slug'), unique=True)
    advertisement_image = ThumbnailField(_('Advertisement Image'), null=True, blank=True, upload_to=_get_upload_path)
    trailer             = models.URLField(_('Trailer'), null=True, blank=True)
    description         = MarkupField(_('Description'), max_length=4096)
    platforms           = models.ManyToManyField(Platform, verbose_name=_('Platforms'))
    project             = models.ForeignKey(Project, verbose_name=_('Project'), null=True, blank=True)
    administrators      = models.ManyToManyField(Persona, verbose_name=_('Administrators'))
    display_mode        = models.PositiveSmallIntegerField(_('Display mode'), choices=DISPLAY_MODES)
    created_at          = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at          = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        ordering = ('display_mode',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Release(models.Model):

    label      = models.CharField(_('Label'), max_length=32)
    platform   = models.ForeignKey(Platform, verbose_name=_('Platform'))
    version    = models.CharField(_('Version'), max_length=32)
    product    = models.ForeignKey(Product, verbose_name=_('Product'), related_name='%(class)ss')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ('platform__pk', 'product__pk')


class PackageRelease(Release):

    def _get_upload_path(self, filename):
        path = 'products/{}/releases/'.format(self.product.slug)
        return os.path.join(path, filename)

    file     = models.FileField(_('File'), upload_to=_get_upload_path)
    download = models.PositiveIntegerField(_('Downloads'), default=0, editable=False)

    class Meta(Release.Meta):
        verbose_name = _('Package release')
        verbose_name_plural = _('Package releases')


class URLRelease(Release):
    url      = models.URLField(_('URL'))
    pageview = models.PositiveIntegerField(_('Page view'), default=0, editable=False)

    class Meta(Release.Meta):
        verbose_name = _('URL release')
        verbose_name_plural = _('URL releases')

class ScreenShot(models.Model):

    def _get_upload_path(self, filename):
        path = 'products/{}/screenshots/%s'.format(self.product.slug)
        return os.path.join(path, filename)

    image   = ThumbnailField(_('Image'), upload_to=_get_upload_path)
    product = models.ForeignKey(Product, verbose_name=_('Product'))

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Screen shot')
        verbose_name_plural = _('Screen shots')
