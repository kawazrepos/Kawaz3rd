from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import PlatformFactory
from .factories import CategoryFactory
from .factories import ProductFactory
from .factories import URLReleaseFactory
from .factories import PackageReleaseFactory
from .factories import Screenshot


class PlatformModelTestCase(TestCase):
    def test_str_returns_platform_label(self):
        """
        str()関数はプラットフォームのラベルを返す
        """
        platform = PlatformFactory(label='iOS')
        self.assertTrue(str(platform), 'iOS')


class CategoryModelTestCase(TestCase):
    def test_str_returns_category_label(self):
        """
        str()関数はカテゴリーのラベルを返す
        """
        category = CategoryFactory(label='シューティングゲーム')
        self.assertTrue(str(category), 'シューティングゲーム')


class ProductModelTestCase(TestCase):
    def test_str_returns_product_title(self):
        """
        str()関数はプロダクトのタイトルを返す
        """
        product = ProductFactory(title='かわずたんシューティング')
        self.assertTrue(str(product), 'かわずたんシューティング')

    def test_display_mode_validation(self):
        """
        `advertisement_image`が指定されていない場合は`display_mode`は
        `tiled`か`normal`しか認められない
        """
        self.assertRaises(ValidationError, ProductFactory,
                          advertisement_image=None,
                          display_mode='featured')
        self.assertIsNotNone(ProductFactory(advertisement_image=None,
                                            display_mode='tiled'))
        self.assertIsNotNone(ProductFactory(advertisement_image=None,
                                            display_mode='normal'))

    def test_get_absolute_url(self):
        """
        get_absolute_url() は '/products/<slug>/' を返す
        """
        slug = 'super-kawaz-adventure'
        expected = '/products/{}/'.format(slug)
        product = ProductFactory(slug=slug)
        self.assertEqual(product.get_absolute_url(), expected)

    def test_members_can_join(self):
        """
        メンバーユーザーは参加することが出来る
        """
        product = ProductFactory()
        roles = ['adam', 'seele', 'nerv', 'children']
        for role in roles:
            previous_count = product.administrators.count()
            product.join(PersonaFactory(role=role))
            self.assertEqual(product.administrators.count(), previous_count+1)

    def test_non_members_cannot_join(self):
        """
        非メンバーユーザーは参加不可
        """
        product = ProductFactory()
        user = PersonaFactory(role='wille')
        self.assertEqual(product.administrators.count(), 0)
        self.assertRaises(PermissionDenied, product.join, user)
        self.assertEqual(product.administrators.count(), 0)

        product = ProductFactory()
        roles = ['wille', None]
        for role in roles:
            previous_count = product.administrators.count()
            user = PersonaFactory(role=role) if role else AnonymousUser()
            self.assertRaises(PermissionDenied, product.join, user)
            self.assertEqual(product.administrators.count(), previous_count)

    def test_administrators_cannot_join(self):
        """
        既に管理者として参加しているメンバーは参加不可
        """
        user = PersonaFactory()
        product = ProductFactory(administrators=(user,))
        self.assertEqual(product.administrators.count(), 1)
        self.assertRaises(PermissionDenied, product.join, user)
        self.assertEqual(product.administrators.count(), 1)

    def test_administrators_can_quit(self):
        """
        管理者として参加しているメンバーは退会可
        """
        user1 = PersonaFactory()
        user2 = PersonaFactory()
        product = ProductFactory(administrators=(user1, user2))
        self.assertEqual(product.administrators.count(), 2)
        product.quit(user1)
        self.assertEqual(product.administrators.count(), 1)
        self.assertFalse(user1 in product.administrators.all())
        self.assertTrue(user2 in product.administrators.all())

    def test_non_administrators_cannot_quit(self):
        """
        管理者として参加していないメンバーは退会不可
        """
        user = PersonaFactory()
        product = ProductFactory()
        self.assertEqual(product.administrators.count(), 0)
        self.assertRaises(PermissionDenied, product.quit, user)
        self.assertEqual(product.administrators.count(), 0)

    def test_last_administrator_cannot_quit(self):
        """
        最後の管理者は退会不可
        """
        user = PersonaFactory()
        product = ProductFactory(administrators=(user,))
        self.assertEqual(product.administrators.count(), 1)
        self.assertRaises(PermissionDenied, product.quit, user)
        self.assertEqual(product.administrators.count(), 1)


class AbstractReleaseBaseModelTestCase(object):
    def test_str_returns_product_title_and_platform_name(self):
        """
        str()関数は"<product_title>(platform_name)"を返す
        """
        package = PackageReleaseFactory()
        self.assertTrue(str(package), 'かわずたんアドベンチャー(Mac)')

class PackageReleaseModelTestCase(TestCase, AbstractReleaseBaseModelTestCase):
    pass


class URLReleaseModelTestCase(TestCase):
    appstore_url = ('https://itunes.apple.com/jp/app/'
                    'wave-weaver/id841280819?mt=8')
    googleplay_url = ('https://play.google.com/store/'
                      'apps/details?id=org.kawaz.Weaver')

    def setUp(self):
        self.appstore_release = URLReleaseFactory(url=self.appstore_url)
        self.googleplay_release = URLReleaseFactory(url=self.googleplay_url)

    def test_is_appstore_works_correctly(self):
        """
        is_appstore() メソッドは AppStore の URL が与えられた時に True を示す
        """
        self.assertTrue(self.appstore_release.is_appstore)
        self.assertFalse(self.googleplay_release.is_appstore)

    def test_is_appstore_works_correctly(self):
        """
        is_googleplay() メソッドは Google Play の URL が与えられた時に True を
        示す
        """
        self.assertFalse(self.appstore_release.is_googleplay)
        self.assertTrue(self.googleplay_release.is_googleplay)

