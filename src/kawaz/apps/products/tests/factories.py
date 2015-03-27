import os
import datetime
from django.utils import timezone
import factory
from kawaz.apps.projects.tests.factories import ProjectFactory
from ..models import Platform
from ..models import Category
from ..models import Product
from ..models import URLRelease
from ..models import PackageRelease
from ..models import Screenshot


class PlatformFactory(factory.DjangoModelFactory):

    class Meta:
        model = Platform

    label = factory.Sequence(lambda n: 'OUYA{}'.format(n))
    icon = "icons/platforms/ouya.png"


class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Category

    label = factory.Sequence(lambda n: 'クソゲー{}'.format(n))
    description = 'クソゲーです'


class ProductFactory(factory.DjangoModelFactory):

    class Meta:
        model = Product

    title = factory.sequence(lambda n: 'かわずたんアドベンチャー{}'.format(n))
    slug = factory.sequence(lambda n: 'kawaz-tan-adventure-{}'.format(n))
    advertisement_image = ('products/kawaz-tan-adventure/'
                           'advertisement_images/kawaztan.png')
    thumbnail = 'products/kawaz-tan-adventure/thumbnails/kawaztan.png'
    trailer = 'http://www.youtube.com/watch?v=0wIGRDKELFg'
    description = 'かわずたんが井戸から飛び出す一大スペクタクルです'
    project = factory.SubFactory(ProjectFactory)
    display_mode = 'featured'
    published_at = datetime.datetime(2009, 10, 15, tzinfo=timezone.utc)

    @factory.post_generation
    def administrators(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.administrators.add(user)

    @factory.post_generation
    def platforms(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for platform in extracted:
                self.platforms.add(platform)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for category in extracted:
                self.categories.add(category)


class ReleaseFactory(factory.DjangoModelFactory):
    label = 'Mac版'
    platform = factory.SubFactory(PlatformFactory)
    version = 'β版'
    product = factory.SubFactory(ProductFactory)


class PackageReleaseFactory(ReleaseFactory):

    class Meta:
        model = PackageRelease

    file_content = 'products/kawaz-tan-adventure/releases/kawaz_mac.zip'

    @factory.post_generation
    def file_content(self, create, extracted=None):
        # ファイル名を与えられたら勝手にパスを生成します
        # release = PackageReleaseFactory(file_content='icon.png',
        #                                 product_slug='kawaztan-game')
        # material.file_content = products/kawaztan-game/releases/icon.png
        if not extracted:
            extracted = 'icon.png'
        content_path = os.path.join(
            'products', self.product.slug, 'releases', extracted,
        )
        self.file_content = content_path
        return content_path


class URLReleaseFactory(ReleaseFactory):

    class Meta:
        model = URLRelease

    url = 'https://itunes.apple.com/jp/app/kawazutantataki!/id447763556?mt=8'


class ScreenshotFactory(factory.DjangoModelFactory):

    class Meta:
        model = Screenshot

    image = 'products/kawaz-tan-adventure/screenshots/cute_kawaz_tan.png'
    product = factory.SubFactory(ProductFactory)
