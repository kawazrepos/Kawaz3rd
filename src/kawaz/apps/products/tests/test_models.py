from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import PlatformFactory
from .factories import CategoryFactory
from .factories import ProductFactory
from .factories import ScreenshotFactory
from .factories import URLReleaseFactory
from .factories import PackageReleaseFactory
from ..models import Category
from ..models import Platform
from ..models import INVALID_PRODUCT_SLUGS


class PlatformModelTestCase(TestCase):
    def test_str_returns_platform_label(self):
        """
        str()関数はプラットフォームのラベルを返す
        """
        platform = PlatformFactory(label='iOS')
        self.assertTrue(str(platform), 'iOS')

    def test_platform_order(self):
        """
        Platformはorderの値が小さい順に並ぶ
        """
        platform0 = PlatformFactory(label='Windows0', order=3)
        platform1 = PlatformFactory(label='Windows1', order=1)
        platform2 = PlatformFactory(label='Windows2', order=2)
        qs = Platform.objects.all()
        self.assertEqual(qs[0], platform1)
        self.assertEqual(qs[1], platform2)
        self.assertEqual(qs[2], platform0)


class CategoryModelTestCase(TestCase):
    def test_str_returns_category_label(self):
        """
        str()関数はカテゴリーのラベルを返す
        """
        category = CategoryFactory(label='シューティングゲーム')
        self.assertTrue(str(category), 'シューティングゲーム')

    def test_category_order(self):
        """
        Categoryはorderの値が小さい順に並ぶ
        """
        category0 = CategoryFactory(label='シューティングゲーム0', order=3)
        category1 = CategoryFactory(label='シューティングゲーム1', order=1)
        category2 = CategoryFactory(label='シューティングゲーム2', order=2)
        qs = Category.objects.all()
        self.assertEqual(qs[0], category1)
        self.assertEqual(qs[1], category2)
        self.assertEqual(qs[2], category0)


class ProductModelTestCase(TestCase):
    def test_product_factory_create_unique_product(self):
        """
        ProductFactory が一意なプロダクトを返すか否か（Ref: issue#68）
        """
        from ..models import Product
        for i in range(5):
            ProductFactory()
        self.assertEqual(Product.objects.count(), 5)

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

    def test_reserved_slug(self):
        """
        INVALID_PRODUCT_SLUGSに指定されている名前はslugとして認められない
        """
        for invalid_slug in INVALID_PRODUCT_SLUGS:
            self.assertRaises(ValidationError,
                              ProductFactory,
                              slug=invalid_slug)

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
    def test_get_absolute_url(self):
        """
        get_absolute_urlでダウンロード用ビューのURLが引ける
        """
        release = PackageReleaseFactory()
        self.assertEqual(release.get_absolute_url(),
                         '/products/package_releases/{}/'.format(release.pk))

    def test_filename(self):
        """
        release.filenameがファイル名を返す
        """
        release = PackageReleaseFactory(
            file_content='path/to/release/my-fantastic-game.zip')
        self.assertEqual(release.filename, 'my-fantastic-game.zip')

    def test_mimetype(self):
        """
        release.mimetypeがMimetypeを返す
        """
        release = PackageReleaseFactory(
            file_content='path/to/release/my-fantastic-game.zip')
        self.assertEqual(release.mimetype, 'application/zip')


class URLReleaseModelTestCase(TestCase, AbstractReleaseBaseModelTestCase):
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

    def test_is_googleplay_works_correctly(self):
        """
        is_googleplay() メソッドは Google Play の URL が与えられた時に True を
        示す
        """
        self.assertFalse(self.appstore_release.is_googleplay)
        self.assertTrue(self.googleplay_release.is_googleplay)

    def test_get_absolute_url(self):
        """
        get_absolute_urlでリダイレクト用ビューのURLが引ける
        """
        release = URLReleaseFactory()
        self.assertEqual(release.get_absolute_url(),
                         '/products/url_releases/{}/'.format(release.pk))

    def test_app_id_with_ios(self):
        """
        iOSアプリのAppIDが取り出せる
        """
        release = URLReleaseFactory(url='https://itunes.apple.com/ja/app/kawazutanjetto!/id922471335?mt=8')
        app_id = release.app_id
        self.assertEqual(app_id, '922471335')

    def test_app_id_with_android(self):
        """
        AndroidアプリのAppIDが取り出せる
        """
        release = URLReleaseFactory(url='https://play.google.com/store/apps/details?id=org.kawaz.KawazJet')
        app_id = release.app_id
        self.assertEqual(app_id, 'org.kawaz.KawazJet')

    def test_app_id_with_other(self):
        """
        その他のアプリのAppIDは空白文字が返ってくる
        """
        release = URLReleaseFactory(url="http://www.google.com")
        app_id = release.app_id
        self.assertEqual(app_id, '')

    def test_is_play_now(self):
        """
        ブラウザゲームはis_play_nowがTrueになる
        """
        release0 = URLReleaseFactory(platform__label='ブラウザ')
        self.assertTrue(release0.is_play_now())
        release1 = URLReleaseFactory(platform__label='iOS')
        self.assertFalse(release1.is_play_now())


class ScreenshotModelTestCase(TestCase):

    def test_screenshot_str(self):
        """
        str(Screenshot)の値が正しい
        """
        product = ProductFactory(title="スーパーかわずたん")
        ss = ScreenshotFactory(product=product)
        self.assertEqual(str(ss), (
            'products/kawaz-tan-adventure/screenshots/'
            'cute_kawaz_tan.png(スーパーかわずたん)'
        ))

    def test_screenshot_relative_name(self):
        """
        Product.screenshotsでスクリーンショットの一覧が取り出せる
        """
        product = ProductFactory()
        ScreenshotFactory(product=product)
        self.assertIsNotNone(product.screenshots)
        self.assertEqual(product.screenshots.count(), 1)
