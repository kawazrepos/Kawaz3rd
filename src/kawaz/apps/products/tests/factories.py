import datetime
import factory
from kawaz.apps.projects.tests.factories import ProjectFactory
from ..models import Platform
from ..models import Category
from ..models import Product
from ..models import URLRelease
from ..models import PackageRelease
from ..models import Screenshot


class PlatformFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Platform
    FACTORY_DJANGO_GET_OR_CREATE = ('label',)

    label = "Mac"
    icon = "icons/platforms/mac.png"


class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category
    FACTORY_DJANGO_GET_OR_CREATE = ('label',)

    label = 'アクションゲーム'
    description = 'アクションゲームです'


class ProductFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Product
    FACTORY_DJANGO_GET_OR_CREATE = ('slug',)

    title = 'かわずたんアドベンチャー'
    slug = 'kawaz-tan-adventure'
    advertisement_image = ('products/kawaz-tan-adventure/'
                           'advertisement_images/kawaztan.png')
    thumbnail = 'products/kawaz-tan-adventure/thumbnails/kawaztan.png'
    trailer = 'http://www.youtube.com/watch?v=0wIGRDKELFg'
    description = 'かわずたんが井戸から飛び出す一大スペクタクルです'
    project = factory.SubFactory(ProjectFactory)
    display_mode = 'featured'
    publish_at = datetime.date(2009, 10, 15)

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


class ReleaseFactory(factory.DjangoModelFactory):
    label = 'Mac版'
    platform = factory.SubFactory(PlatformFactory)
    version = 'β版'
    product = factory.SubFactory(ProductFactory)


class PackageReleaseFactory(ReleaseFactory):
    FACTORY_FOR = PackageRelease

    file_content = 'products/kawaz-tan-adventure/releases/kawaz_mac.zip'


class URLReleaseFactory(ReleaseFactory):
    FACTORY_FOR = URLRelease

    url = 'https://itunes.apple.com/jp/app/kawazutantataki!/id447763556?mt=8'


class ScreenshotFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Screenshot

    image = 'products/kawaz-tan-adventure/screenshots/cute_kawaz_tan.png'
    product = factory.SubFactory(ProductFactory)

