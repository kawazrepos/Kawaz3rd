import factory
from ..models import Platform
from ..models import Category
from ..models import Product
from ..models import URLRelease
from ..models import PackageRelease
from ..models import ScreenShot

from kawaz.apps.projects.tests.factories import ProjectFactory

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
    advertisement_image = 'products/kawaz-tan-adventure/advertisement_images/kawaztan.png'
    trailer = 'http://www.youtube.com/watch?v=0wIGRDKELFg'
    description = 'かわずたんが井戸から飛び出す一大スペクタクルです'
    project = factory.SubFactory(ProjectFactory)
    display_mode = 0

class ReleaseFactory(factory.DjangoModelFactory):

    label = 'Mac版'
    platform = factory.SubFactory(PlatformFactory)
    version = 'β版'
    product = factory.SubFactory(ProductFactory)

class PackageReleaseFactory(ReleaseFactory):
    FACTORY_FOR = PackageRelease

    file = 'products/kawaz-tan-adventure/releases/kawaz_mac.zip'

class URLReleaseFactory(ReleaseFactory):
    FACTORY_FOR = URLRelease

    url = 'https://itunes.apple.com/jp/app/kawazutantataki!/id447763556?mt=8'

class ScreenShotFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ScreenShot

    image = 'products/kawaz-tan-adventure/screenshots/cute_kawaz_tan.png'
    product = factory.SubFactory(ProductFactory)
