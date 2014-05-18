import os
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from markupfield.fields import MarkupField
from thumbnailfield.fields import ThumbnailField

from kawaz.core.db.decorators import validate_on_save
from kawaz.core.personas.models import Persona
from kawaz.apps.projects.models import Project


class Platform(models.Model):
    '''
    Model for supports platform of products
    e.g. Windows, Mac, Browser, iOS or PS Vita etc...
    '''

    def _get_upload_path(self, filename):
        basedir = os.path.join('icons', 'platforms', self.label.lower())
        return os.path.join(basedir, filename)


    label = models.CharField(_('Label'), max_length=32)
    icon  = models.ImageField(_('Icon'), upload_to=_get_upload_path)

    class Meta:
        ordering = ('label',)
        verbose_name = _('Platform')
        verbose_name_plural = _('Platforms')

    def __str__(self):
        return self.label

class Category(models.Model):
    '''
    Model for categories of products
    e.g. ACT, STG, ADV or Casual Game etc...
    '''

    label       = models.CharField(_('Label'), max_length=32, unique=True)
    description = models.CharField(_('Description'), max_length=128)

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.label

@validate_on_save
class Product(models.Model):
    '''
    Model for products
    '''

    def _get_advertisement_image_upload_path(self, filename):
        basedir = os.path.join('products', self.slug, 'advertisement_images')
        return os.path.join(basedir, filename)

    def _get_thumbnail_upload_path(self, filename):
        basedir = os.path.join('products', self.slug, 'thumbnails')
        return os.path.join(basedir, filename)

    DISPLAY_MODES = (
        (0, _('Featured')),
        (1, _('Tiled')),
        (2, _('Normal')),
    )

    title               = models.CharField(_('Title'), max_length=128, unique=True)
    slug                = models.SlugField(_('Slug'), unique=True, help_text=_('You can not modify this field later.'))
    advertisement_image = ThumbnailField(_('Advertisement Image'), null=True, blank=True,
                                         upload_to=_get_advertisement_image_upload_path, patterns=settings.ADVERTISEMENT_IMAGE_SIZE_PATTERNS,
                                         help_text=_('This image will be insert on top page. Aspect ratio of this image should be 16:9.')
                                        )
    thumbnail           = ThumbnailField(_('Thumbnail'),
                                         upload_to=_get_thumbnail_upload_path, patterns=settings.PRODUCT_THUMBNAIL_SIZE_PATTERNS,
                                         help_text=_('This image will be used as product thumbnail. Aspect ratio of this image should be 16:9.')
                                        )
    trailer             = models.URLField(_('Trailer'), null=True, blank=True,
                                          help_text='Enter URL of your trailer on YouTube, then you can embed the trailer.'
                                          )
    description         = MarkupField(_('Description'), max_length=4096, markup_type='markdown')
    platforms           = models.ManyToManyField(Platform, verbose_name=_('Platforms'))
    categories          = models.ManyToManyField(Category, verbose_name=_('Categories'))
    project             = models.ForeignKey(Project, verbose_name=_('Project'), null=True, blank=True)
    administrators      = models.ManyToManyField(Persona, verbose_name=_('Administrators'))
    display_mode        = models.PositiveSmallIntegerField(_('Display mode'), choices=DISPLAY_MODES,
                                                           help_text=_("""Display mode on Kawaz top. '
                                                                       'If this have no `Advertisement Image`, You can't choose `Featured`.""")
                                                           )
    publish_at          = models.DateField(_('Publish at'))
    created_at          = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at          = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        ordering = ('display_mode',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = (
            ('join_product', 'Can join to the product'),
            ('quit_product', 'Can quit from the product'),
        )

    def __str__(self):
        return self.title

    def clean(self):
        if not self.advertisement_image and self.display_mode == 0:
            # advertisement_imageがセットされていないときはdisplay_modeをFeaturedに設定できない
            raise ValidationError(_('''`display_mode` is not allowed for 'Featured' without setting `advertisement_image`'''))

    def join(self, user, save=True):
        """
        指定されたユーザーを管理者にする

        ユーザーに参加権限がない場合は `PermissionDenied` を投げる
        """
        if not user.has_perm('products.join_product', self):
            raise PermissionDenied
        self.administrators.add(user)
        if save:
            self.save()

    def quit(self, user, save=True):
        """
        指定されたユーザーを管理者から外す

        ユーザーに脱退権限がない場合は `PermissionDenied` を投げる
        """
        if not user.has_perm('products.quit_product', self):
            raise PermissionDenied
        self.administrators.remove(user)
        if save:
            self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('products_product_detail', (), {
            'slug' : self.slug
        })


class Release(models.Model):
    '''
    Abstract model for product releases
    '''

    label      = models.CharField(_('Label'), max_length=32)
    platform   = models.ForeignKey(Platform, verbose_name=_('Platform'))
    version    = models.CharField(_('Version'), max_length=32)
    product    = models.ForeignKey(Product, verbose_name=_('Product'), related_name='%(class)ss')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ('platform__pk', 'product__pk')

    def __str__(self):
        return "{}({})".format(str(self.product), str(self.platform))

class PackageRelease(Release):
    '''
    Model for file contains release
    developers can host game binaries on Kawaz
    '''

    def _get_upload_path(self, filename):
        basedir = os.path.join('products', self.product.slug, 'releases')
        return os.path.join(basedir, filename)

    file     = models.FileField(_('File'), upload_to=_get_upload_path)
    download = models.PositiveIntegerField(_('Downloads'), default=0, editable=False)

    class Meta(Release.Meta):
        verbose_name = _('Package release')
        verbose_name_plural = _('Package releases')


class URLRelease(Release):
    '''
    Model for URL release
    If games are hosted on other website, developers can link to there.
    e.g. Google Play, iTunes App Store etc...
    '''


    url      = models.URLField(_('URL'))
    pageview = models.PositiveIntegerField(_('Page view'), default=0, editable=False)

    class Meta(Release.Meta):
        verbose_name = _('URL release')
        verbose_name_plural = _('URL releases')

    @property
    def is_appstore(self):
        '''Return `True` if this release is hosted on App Store'''
        # ProductページにApp Storeのバッジを置いたりするのに使います
        return self.url.startswith('https://itunes.apple.com')

    @property
    def is_googleplay(self):
        '''Return `True` if this release is hosted on Google Play'''
        # ProductページにGoogle Playのバッジを置いたりするのに使います
        return self.url.startswith('https://play.google.com')

class ScreenShot(models.Model):
    '''
    Model for product screen shots
    developers can attach as many screenshots as they would like.
    '''

    def _get_upload_path(self, filename):
        basedir = os.path.join('products', self.product.slug, 'screenshots')
        return os.path.join(basedir, filename)

    image   = ThumbnailField(_('Image'), upload_to=_get_upload_path,
                             patterns=settings.SCREENSHOT_IMAGE_SIZE_PATTERNS)
    product = models.ForeignKey(Product, verbose_name=_('Product'))

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Screen shot')
        verbose_name_plural = _('Screen shots')

    def __str__(self):
        return '{}({})'.format(self.image.name, self.product.title)

from kawaz.core.permissions.logics import ChildrenPermissionLogic
from permission import add_permission_logic
from .perms import ProductPermissionLogic
add_permission_logic(Product, ChildrenPermissionLogic(
    add_permission=True,
    change_permission=False,
    delete_permission=False
))
add_permission_logic(Product, ProductPermissionLogic())
