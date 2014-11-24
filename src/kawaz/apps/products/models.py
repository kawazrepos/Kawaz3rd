import mimetypes
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from thumbnailfield.fields import ThumbnailField
from kawaz.core.db.decorators import validate_on_save
from kawaz.core.personas.models import Persona
from kawaz.apps.projects.models import Project


PRODUCT_THUMBNAIL_SIZE_PATTERNS = {
    'huge': (512, 288,),
    'large': (172, 96,),
    'middle': (86, 48,),
    'small': (43, 24,),
}
ADVERTISEMENT_IMAGE_SIZE_PATTERNS = {
    'huge': (512, 288,),
    'large': (172, 96,),
    'middle': (86, 48,),
    'small': (43, 24,),
}
SCREENSHOT_IMAGE_SIZE_PATTERNS = {
    None: None,
}


class Platform(models.Model):
    """
    プロダクトがサポートしているプラットフォームを表すモデル

    e.g. Windows, Mac, Browser, iOS, PS Vita など
    """

    def _get_upload_path(self, filename):
        basedir = os.path.join('products', 'platforms', self.label.lower())
        return os.path.join(basedir, filename)

    label = models.CharField(_('Label'), max_length=32, unique=True)
    icon = models.ImageField(_('Icon'), upload_to=_get_upload_path)
    order = models.PositiveSmallIntegerField(
        _('Order'), help_text=('この値が小さい順に並びます'), default=0)

    class Meta:
        ordering = ('order', 'pk',)
        verbose_name = _('Platform')
        verbose_name_plural = _('Platforms')

    def __str__(self):
        return self.label


class Category(models.Model):
    """
    プロダクトが所属するカテゴリーを表すモデル

    e.g. ACT, STG, ADV など
    """
    label = models.CharField(_('Label'), max_length=32, unique=True)
    description = models.CharField(_('Description'), max_length=128)
    order = models.PositiveSmallIntegerField(
        _('Order'), help_text='この値が小さい順に並びます', default=0)

    class Meta:
        ordering = ('order', 'pk',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.label


@validate_on_save
class Product(models.Model):
    """
    完成したプロダクトを表すモデル

    メンバーであれば誰でも作成・管理可能
    """

    def _get_advertisement_image_upload_path(self, filename):
        basedir = os.path.join('products', self.slug, 'advertisement_images')
        return os.path.join(basedir, filename)

    def _get_thumbnail_upload_path(self, filename):
        basedir = os.path.join('products', self.slug, 'thumbnails')
        return os.path.join(basedir, filename)

    DISPLAY_MODES = (
        ('featured', _(
            'Fetured: Displayed in the curled cell and the tiled cell '
            'on the top page'
        )),
        ('tiled', _(
            'Tiled: Displayed in the tiled cell on the top page'
        )),
        ('normal', _(
            'Normal: Displayed only in tiled cell on the detailed page'
        )),
    )

    # 必須フィールド
    title = models.CharField(_('Title'), max_length=128, unique=True)
    slug = models.SlugField(_('Product slug'), unique=True,
                            help_text=_("It will be used on the url of the "
                                        "product thus it only allow "
                                        "alphabetical or numeric "
                                        "characters, underbar ('_'), and "
                                        "hyphen ('-'). "
                                        "Additionally this value cannot be "
                                        "modified for preventing the URL "
                                        "changes."))
    thumbnail = ThumbnailField(
        _('Thumbnail'),
        upload_to=_get_thumbnail_upload_path,
        patterns=PRODUCT_THUMBNAIL_SIZE_PATTERNS,
        help_text=_("This would be used as a product thumbnail image. "
                    "The aspect ratio of the image should be 16:9."
                    "We recommend the image size to be 800 * 450."))
    description = models.TextField(_('Description'), max_length=4096)

    # 省略可能フィールド
    advertisement_image = ThumbnailField(
        _('Advertisement Image'),
        null=True, blank=True,
        upload_to=_get_advertisement_image_upload_path,
        patterns=ADVERTISEMENT_IMAGE_SIZE_PATTERNS,
        help_text=_("This would be used in the top page. "
                    "The aspect ratio of the image should be 16:9"
                    "We recommend the image size to be 800 * 450"))
    trailer = models.URLField(
        _('Trailer'), null=True, blank=True,
        help_text=_("Enter URL of your trailer movie on the YouTube. "
                    "The movie would be embeded to the product page."))
    project = models.OneToOneField(Project, verbose_name=_('Project'),
                                   null=True, blank=True,
                                   related_name='product')
    platforms = models.ManyToManyField(Platform, verbose_name=_('Platforms'))
    categories = models.ManyToManyField(Category,
                                        verbose_name=_('Categories'))
    contact_info = models.CharField(
        _('Contact info'), default='', blank=True, max_length=256,
        help_text=_(
            "Fill your contact info for visitors, "
            "e.g. Twitter account, Email address or Facebook account"))
    published_at = models.DateField(
        _('Published at'),
        help_text=_(
            "If this product have been already released, "
            "please fill the date."))
    administrators = models.ManyToManyField(Persona,
                                            verbose_name=_('Administrators'))

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    last_modifier = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name=_('Last modified by'),
                                      editable=False, null=True,
                                      related_name='last_modified_products')

    #
    # Productの表示順番を制御する値です。Formsでexclude設定されるため通常
    # ユーザーからは変更できません（adminサイトでの修正）
    #
    # featured: トップページのカルーセル + トップページにタイル表示されます。
    #           設定するにはadvertisement_imageの設定が必要です
    # tiled : トップページにタイル表示されます。
    #         タイル表示は thumbnails が使われます
    # normal : トップページには表示されず、see more内でのみタイル表示されます
    #
    display_mode = models.CharField(
        _('Display mode'),
        max_length=10, choices=DISPLAY_MODES, default='normal',
        help_text=_(
            "How the product displayed on the top page. "
            "To use 'Featured', an 'Advertisement image' is required."
        ))

    class Meta:
        ordering = ('display_mode', '-published_at',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = (
            ('join_product', 'Can join to the product'),
            ('quit_product', 'Can quit from the product'),
        )

    def __str__(self):
        return self.title

    def clean(self):
        if not self.advertisement_image and self.display_mode == 'featured':
            # advertisement_imageがセットされていないときは
            # display_modeをfeaturedに設定できない
            raise ValidationError(_(
                "Display mode 'Feature' requires 'Advertisement image'"
            ))
        if self.slug == 'platforms':
            raise ValidationError(_(
                "A product slug 'platforms' is reserved."
            ))

    def join(self, user):
        """
        指定されたユーザーを管理者にする

        ユーザーに参加権限がない場合は `PermissionDenied` を投げる
        """
        if not user.has_perm('products.join_product', self):
            raise PermissionDenied
        self.administrators.add(user)

    def quit(self, user):
        """
        指定されたユーザーを管理者から外す

        ユーザーに脱退権限がない場合は `PermissionDenied` を投げる
        """
        if not user.has_perm('products.quit_product', self):
            raise PermissionDenied
        self.administrators.remove(user)

    @models.permalink
    def get_absolute_url(self):
        return ('products_product_detail', (), {
            'slug': self.slug
        })


class AbstractRelease(models.Model):
    """
    リリース形態のアブストラクトモデル
    """
    label = models.CharField(pgettext_lazy('Release name', 'Label'),
                             max_length=32)
    platform = models.ForeignKey(Platform, verbose_name=_('Platform'))
    version = models.CharField(_('Version'), max_length=32,
                               default='', blank=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'),
                                related_name='%(class)ss', editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ('platform__pk', 'product__pk')

    def __str__(self):
        return "{}({})".format(str(self.product), str(self.platform))


class PackageRelease(AbstractRelease):
    """
    ファイル添付形式でのリリースモデル
    """

    def _get_upload_path(self, filename):
        basedir = os.path.join('products', self.product.slug, 'releases')
        return os.path.join(basedir, filename)

    file_content = models.FileField(_('File'), upload_to=_get_upload_path)
    downloads = models.PositiveIntegerField(
        _('Downloads'), default=0,
        editable=False,
        help_text=_("The number of downloads"))

    class Meta(AbstractRelease.Meta):
        verbose_name = _('Package release')
        verbose_name_plural = _('Package releases')

    @models.permalink
    def get_absolute_url(self):
        return ('products_package_release_detail', (self.pk,), {})

    @property
    def filename(self):
        """
        ファイル名を返します
        """
        return os.path.split(self.file_content.name)[1]

    @property
    def mimetype(self):
        """
        Mimetypeを返します
        """
        mime_type_guess = mimetypes.guess_type(self.filename)
        return mime_type_guess[0]

class URLRelease(AbstractRelease):
    """
    URL指定形式でのリリースモデル。主に外部ホスティングでのリリース用

    e.g. iTunes App Store, Google Play, Vector など
    """
    url = models.URLField(_('URL'))
    pageview = models.PositiveIntegerField(
        _('Page view'), default=0,
        editable=False,
        help_text=_("The number of page views"))

    class Meta(AbstractRelease.Meta):
        verbose_name = _('URL release')
        verbose_name_plural = _('URL releases')

    @property
    def is_appstore(self):
        """App Store の URL か否か"""
        # ProductページにApp Storeのバッジを置いたりするのに使います
        return self.url.startswith('https://itunes.apple.com')

    @property
    def is_googleplay(self):
        """Google Play の URL か否か"""
        # ProductページにGoogle Playのバッジを置いたりするのに使います
        return self.url.startswith('https://play.google.com')

    @models.permalink
    def get_absolute_url(self):
        return ('products_url_release_detail', (self.pk,), {})


class Screenshot(models.Model):
    """
    プロダクトのスクリーンショットモデル

    プロダクト管理者は何枚でもプロダクトに関連付けることが出来る
    """

    def _get_upload_path(self, filename):
        basedir = os.path.join('products', self.product.slug, 'screenshots')
        return os.path.join(basedir, filename)

    image = ThumbnailField(
        _('Image'), upload_to=_get_upload_path,
        patterns=SCREENSHOT_IMAGE_SIZE_PATTERNS)
    product = models.ForeignKey(
        Product, verbose_name=_('Product'), editable=False,
        related_name='screenshots')

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Screen shot')
        verbose_name_plural = _('Screen shots')

    def __str__(self):
        return '{}({})'.format(self.image.name, self.product.title)


from permission import add_permission_logic
from .perms import ProductPermissionLogic
from kawaz.core.personas.perms import ChildrenPermissionLogic
add_permission_logic(Product, ChildrenPermissionLogic(
    add_permission=True,
    change_permission=False,
    delete_permission=False
))
add_permission_logic(Product, ProductPermissionLogic())

from .activity import ProductActivityMediator
from activities.registry import registry
registry.register(Product, ProductActivityMediator())

from .activity import ReleaseActivityMediator
registry.register(PackageRelease, ReleaseActivityMediator())
registry.register(URLRelease, ReleaseActivityMediator())

from .activity import ScreenshotActivityMediator
registry.register(Screenshot, ScreenshotActivityMediator())
