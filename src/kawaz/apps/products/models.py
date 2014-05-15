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
    title               = models.CharField(_('Title'), max_length=128, unique=True)
    slug                = models.SlugField(_('Slug'), unique=True)
    advertisement_image = ThumbnailField(_('Advertisement Image'), null=True, blank=True)
    trailer             = models.URLField(_('Trailer'), null=True, blank=True)
    description         = MarkupField(_('Description'), max_length=4096)
    platforms           = models.ManyToManyField(Platform, verbose_name=_('Platforms'))
    project             = models.ForeignKey(Project, verbose_name=_('Project'), null=True, blank=True)
    administrators      = models.ManyToManyField(Persona, verbose_name=_('Administrators'))
    display_mode        = models.IntegerField()
    created_at          = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at          = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        ordering = ('display_mode',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Release(models.Model):
    label      = models.CharField(_('labels'), max_length=32)
    platform   = models.ForeignKey(Platform, verbose_name=_('Platform'))
    version    = models.CharField(_('Version'), max_length=32)
    product    = models.ForeignKey(Product, verbose_name=_('Product'), related_name='%(class)ss')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ('platform__pk', 'product__pk')


class PackageRelease(Release):
    file     = models.FileField(_('File'))
    download = models.PositiveIntegerField(_('Downloads'), default=0, editable=False)

    class Meta(Release.Meta):
        verbose_name = _('PackageRelease')
        verbose_name_plural = _('PackageReleases')


class URLRelease(Release):
    url      = models.URLField(_('URL'))
    pageview = models.PositiveIntegerField(_('Page view'), default=0, editable=False)

    class Meta(Release.Meta):
        verbose_name = _('URLRelease')
        verbose_name_plural = _('URLReleases')

class ScreenShot(models.Model):
    image   = ThumbnailField(_('Image'))
    product = models.ForeignKey(Product, verbose_name=_('Product'))

    class Meta:
        ordering = _('pk',)
        verbose_name = _('Screenshot')
        verbose_name_plural = _('Screenshots')
