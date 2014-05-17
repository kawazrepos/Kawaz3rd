from django.test import TestCase
from django.core.exceptions import ValidationError
from .factories import PlatformFactory
from .factories import CategoryFactory
from .factories import ProductFactory
from .factories import URLReleaseFactory
from .factories import PackageReleaseFactory
from .factories import ScreenShot

class PlatformModelTestCase(TestCase):

    def test_str_returns_platform_label(self):
        '''
        Tests str(platform) returns a label of the platform
        '''
        platform = PlatformFactory(label='iOS')
        self.assertTrue(str(platform), 'iOS')


class CategoryModelTestCase(TestCase):

    def test_str_returns_category_label(self):
        '''
        Tests str(category) returns a label of the category
        '''
        category = CategoryFactory(label='シューティングゲーム')
        self.assertTrue(str(category), 'シューティングゲーム')


class ProductModelTestCase(TestCase):

    def test_str_returns_product_title(self):
        '''
        Tests str(category) returns a title of the product
        '''
        product = ProductFactory(title='かわずたんシューティング')
        self.assertTrue(str(product), 'かわずたんシューティング')

    def test_display_mode_validation(self):
        '''
        Tests the validation that without `advertisement_image`, `display_mode` must be `Text`.
        '''
        self.assertRaises(ValidationError, ProductFactory, advertisement_image=None, display_mode=0)
        self.assertRaises(ValidationError, ProductFactory, advertisement_image=None, display_mode=1)
        self.assertRaises(ValidationError, ProductFactory, advertisement_image=None, display_mode=2)
        self.assertIsNotNone(ProductFactory(advertisement_image=None, display_mode=3))

    def test_get_absolute_url(self):
        """
        Tests get_absolute_url() returns '/products/<slug>/'.
        """
        product = ProductFactory(slug='super-kawaz-adventure')
        self.assertEqual(product.get_absolute_url(), '/products/super-kawaz-adventure/')


class PackageReleaseModelTestCase(TestCase):

    def test_str_returns_correct_value(self):
        '''
        Tests str(package_release) returns a text as "<product_title>(platform_name)"
        '''
        package = PackageReleaseFactory()
        self.assertTrue(str(package), 'かわずたんアドベンチャー(Mac)')


class URLReleaseModelTestCase(TestCase):

    def test_str_returns_correct_value(self):
        '''
        Tests str(url_release) returns a text as "<product_title>(platform_name)"
        '''
        release = URLReleaseFactory()
        self.assertTrue(str(release), 'かわずたんアドベンチャー(Mac)')

    def test_is_appstore_works_correctly(self):
        '''
        Tests if URL is for App Store, is_appstore returns True
        '''
        release = URLReleaseFactory(url='https://itunes.apple.com/jp/app/wave-weaver/id841280819?mt=8')
        self.assertTrue(release.is_appstore)
        release2 = URLReleaseFactory(url='https://play.google.com/store/apps/details?id=org.kawaz.Weaver')
        self.assertFalse(release2.is_appstore)

    def test_is_googleplay_works_correctly(self):
        '''
        Tests if URL is for Google Play, is_googleplay returns True
        '''
        release = URLReleaseFactory(url='https://play.google.com/store/apps/details?id=org.kawaz.Weaver')
        self.assertTrue(release.is_googleplay)
        release2 = URLReleaseFactory(url='https://itunes.apple.com/jp/app/wave-weaver/id841280819?mt=8')
        self.assertFalse(release2.is_googleplay)
