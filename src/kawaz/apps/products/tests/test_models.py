from django.test import TestCase
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