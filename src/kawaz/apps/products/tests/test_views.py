import os
import datetime
import itertools
from contextlib import ExitStack
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Screenshot
from ..models import URLRelease
from ..models import PackageRelease

from ..models import Product
from .factories import ProductFactory
from .factories import PlatformFactory
from .factories import CategoryFactory

TEST_FILENAME = os.path.join(os.path.dirname(__file__),
                             'data', 'kawaztan.png')


class ViewTestCaseBase(TestCase):
    def setUp(self):
        self.members = (
            PersonaFactory(role='adam'),
            PersonaFactory(role='seele'),
            PersonaFactory(role='nerv'),
            PersonaFactory(role='children'),
        )
        self.non_members = (
            PersonaFactory(role='wille'),
            AnonymousUser(),
        )
        self.platform = PlatformFactory()
        self.category = CategoryFactory()

    def prefer_login(self, user):
        if user.is_authenticated():
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))


class ProductDetailViewTestCase(ViewTestCaseBase):
    def test_anyone_can_see_product_detail(self):
        """
        プロダクト詳細は誰でも閲覧可能
        """
        product = ProductFactory(slug='super-kawaztan-adventure')
        for user in itertools.chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get('/products/super-kawaztan-adventure/')
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'products/product_detail.html')
            self.assertEqual(r.context['object'], product)


class ProductListViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.p0 = PlatformFactory()
        self.p1 = PlatformFactory()
        self.c0 = CategoryFactory()
        self.c1 = CategoryFactory()

    def test_anyone_can_see_product_list(self):
        """
        プロダクトリストは誰でも閲覧可能
        """
        product = ProductFactory()
        for user in itertools.chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get('/products/')
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'products/product_list.html')
            self.assertTrue(product in r.context['filter'])

    def test_list_with_platforms(self):
        """
        プロダクトリストでPlatformのfilterが有効になっている
        """
        product1 = ProductFactory(platforms=(self.p0,))
        product2 = ProductFactory(platforms=(self.p1,))
        for user in itertools.chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get('/products/?platforms={}'.format(self.p0.pk))
            self.assertTemplateUsed(r, 'products/product_list.html')
            self.assertEqual(len(r.context['filter']), 1)
            self.assertTrue(product1 in r.context['filter'])
            self.assertFalse(product2 in r.context['filter'])

    def test_list_with_categories(self):
        """
        プロダクトリストでCategoryのfilterが有効になっている
        """
        product1 = ProductFactory(categories=(self.c0,))
        # product2 = ProductFactory(categories=[self.c1,])
        self.prefer_login(self.members[0])
        r = self.client.get('/products/?categories={}'.format(self.c0.pk))
        self.assertTemplateUsed(r, 'products/product_list.html')
        self.assertEqual(len(r.context['filter']), 1)
        self.assertTrue(product1 in r.context['filter'])


class ProductCreateViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.product_kwargs = {
            'title': 'かわずたんファンタジー',
            'slug': 'kawaztan-fantasy',
            'thumbnail': 'thumbnail.png',
            'publish_at': datetime.date.today(),
            'platforms': (1,),
            'categories': (1,),
            'administrators': (1,),
            'description': '剣と魔法の物語です',
            'screenshots-TOTAL_FORMS': 0,           # No screenshots
            'screenshots-INITIAL_FORMS': 0,
            'screenshots-MAX_NUM_FORMS': 1000,
            'url_releases-TOTAL_FORMS': 0,          # No URL release
            'url_releases-INITIAL_FORMS': 0,
            'url_releases-MAX_NUM_FORMS': 1000,
            'package_releases-TOTAL_FORMS': 0,      # No package release
            'package_releases-INITIAL_FORMS': 0,
            'package_releases-MAX_NUM_FORMS': 1000,
        }
        self.image_file = TEST_FILENAME
        self.platform = PlatformFactory()

    def test_non_members_cannot_see_create_view(self):
        """
        非メンバーはプロダクト作成画面に行けない
        """
        login_url = settings.LOGIN_URL+'?next=/products/create/'
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get('/products/create/')
            self.assertRedirects(r, login_url)

    def test_members_can_see_create_view(self):
        """
        メンバーはプロダクト作成画面を見ることが出来る
        """
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get('/products/create/')
            self.assertTemplateUsed(r, 'products/product_form.html')
            self.assertFalse('object' in r.context_data)

    def test_non_members_cannot_create_product(self):
        """
        非メンバーはプロダクトの作成が出来ない
        """
        login_url = settings.LOGIN_URL+'?next=/products/create/'
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.post('/products/create/', self.product_kwargs)
            self.assertRedirects(r, login_url)

    def test_contact_info_initial_value(self):
        """
        Contact infoの初期値が
        ニックネーム: メールアドレス
        になっている
        """
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            r = self.client.get('/products/create/')
            form = r.context['form']
            contact_info = "{}: {}".format(user.nickname, user.email)
            self.assertEqual(form.fields['contact_info'].initial, contact_info)

    def test_members_can_create_product(self):
        """
        メンバーはプロダクトを作成することが出来る
        """
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post('/products/create/', self.product_kwargs)
            self.assertRedirects(r, '/products/kawaztan-fantasy/')
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=i+1)
            self.assertEqual(e.pk, i+1)
            self.assertEqual(e.title, 'かわずたんファンタジー')
            self.assertTrue(user in e.administrators.all())
            self.assertEqual(e.administrators.count(), 1)
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 重複を避けるため削除する
            e.delete()

    def test_set_last_modifier_via_create_view(self):
        """
        プロダクト作成時にlast_modifierが設定される
        """
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post('/products/create/', self.product_kwargs)
            self.assertRedirects(r, '/products/kawaztan-fantasy/')
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=i+1)
            self.assertEqual(e.last_modifier, user)
            # 重複を避けるため削除する
            e.delete()

    def test_member_can_create_screenshot_via_product_form(self):
        """
        メンバーはプロダクトフォームからScreenshotモデルも作成できる
        """
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            # Note:
            #   f1, f2 と分けているのは 読み込み後に seek 位置が変更され
            #   再度読みこもうとした場合に seek 位置を戻す必要があるが、
            #   そういう処理がライブラリに無い。したがって同じファイル
            #   オブジェクトを共有できないため、二つに分けている
            with ExitStack() as stack:
                f1 = stack.enter_context(open(self.image_file, 'rb'))
                f2 = stack.enter_context(open(self.image_file, 'rb'))
                self.product_kwargs.update({
                    'thumbnail': f1,
                    'screenshots-TOTAL_FORMS': 1,
                    'screenshots-0-image': f2,
                })
                r = self.client.post('/products/create/', self.product_kwargs)
            self.assertRedirects(r, '/products/kawaztan-fantasy/')

            self.assertEqual(Screenshot.objects.count(), 1)
            obj = Screenshot.objects.get(pk=i+1)
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 重複を避けるため削除する（プロダクトの削除も忘れずに）
            obj.product.delete()
            obj.delete()

    def test_member_can_create_url_release_via_product_form(self):
        """
        メンバーはプロダクトフォームからURLReleaseモデルも作成できる
        """
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs.update({
                    'thumbnail': f,
                    'url_releases-TOTAL_FORMS': 1,
                    'url_releases-0-label': 'Android版',
                    'url_releases-0-version': 'Version3.14',
                    'url_releases-0-platform': self.platform.pk,
                    'url_releases-0-url': 'http://play.google.com',
                })
                r = self.client.post('/products/create/', self.product_kwargs)
            self.assertRedirects(r, '/products/kawaztan-fantasy/')

            self.assertEqual(URLRelease.objects.count(), 1)
            obj = URLRelease.objects.get(pk=i+1)
            self.assertEqual(obj.label, 'Android版')
            self.assertEqual(obj.version, 'Version3.14')
            self.assertEqual(obj.platform, self.platform)
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 重複を避けるため削除する（プロダクトの削除も忘れずに）
            obj.product.delete()
            obj.delete()

    def test_member_can_create_package_release_via_product_form(self):
        """
        メンバーはプロダクトフォームからPackageReleaseモデルも作成できる
        """
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            # Note:
            #   f1, f2 と分けているのは 読み込み後に seek 位置が変更され
            #   再度読みこもうとした場合に seek 位置を戻す必要があるが、
            #   そういう処理がライブラリに無い。したがって同じファイル
            #   オブジェクトを共有できないため、二つに分けている
            with ExitStack() as stack:
                f1 = stack.enter_context(open(self.image_file, 'rb'))
                f2 = stack.enter_context(open(self.image_file, 'rb'))
                self.product_kwargs.update({
                    'thumbnail': f1,
                    'package_releases-TOTAL_FORMS': 1,
                    'package_releases-0-label': 'Android版',
                    'package_releases-0-version': 'Version3.14',
                    'package_releases-0-platform': self.platform.pk,
                    'package_releases-0-file_content': f2,
                })
                r = self.client.post('/products/create/', self.product_kwargs)
            self.assertRedirects(r, '/products/kawaztan-fantasy/')

            self.assertEqual(PackageRelease.objects.count(), 1)
            obj = PackageRelease.objects.get(pk=i+1)
            self.assertEqual(obj.label, 'Android版')
            self.assertEqual(obj.version, 'Version3.14')
            self.assertEqual(obj.platform, self.platform)
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 重複を避けるため削除する（プロダクトの削除も忘れずに）
            obj.product.delete()
            obj.delete()


class ProductUpdateViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.administrator = PersonaFactory(username='administrator')
        self.product = ProductFactory(
            title="かわずたんのゲームだよ☆",
            administrators=(self.administrator,)
        )
        self.product_kwargs = {
            'title': 'クラッカーだよ！！！',
            'publish_at': datetime.date.today(),
            'platforms': (1,),
            'categories': (1,),
            'administrators': (1,),
            'description': '剣と魔法の物語です',
            'screenshots-TOTAL_FORMS': 0,           # No screenshots
            'screenshots-INITIAL_FORMS': 1,
            'screenshots-MAX_NUM_FORMS': 1000,
            'url_releases-TOTAL_FORMS': 0,          # No URL release
            'url_releases-INITIAL_FORMS': 1,
            'url_releases-MAX_NUM_FORMS': 1000,
            'package_releases-TOTAL_FORMS': 0,      # No package release
            'package_releases-INITIAL_FORMS': 1,
            'package_releases-MAX_NUM_FORMS': 1000,
        }
        self.image_file = TEST_FILENAME

    def test_non_members_cannot_see_product_update_view(self):
        """
        非メンバーはプロダクト編集ページは見ることが出来ない
        """
        login_url = settings.LOGIN_URL+'?next=/products/1/update/'
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get('/products/1/update/')
            self.assertRedirects(r, login_url)

    def test_non_administrators_cannot_see_product_update_view(self):
        """
        非管理メンバーはプロジェクト編集ページは見ることが出来ない
        """
        login_url = settings.LOGIN_URL+'?next=/products/1/update/'
        # adam は全ての権限を持つため除外
        for user in self.members[1:]:
            self.prefer_login(user)
            r = self.client.get('/products/1/update/')
            self.assertRedirects(r, login_url)

    def test_administrators_can_view_product_update_view(self):
        """
        管理メンバーはプロジェクト編集ページを見ることが出来る
        """
        # adam はすべての権限を持つため追加
        for user in [self.members[0], self.administrator]:
            self.prefer_login(user)
            r = self.client.get('/products/1/update/')
            self.assertTemplateUsed(r, 'products/product_form.html')
            self.assertTrue('object' in r.context_data)
            self.assertEqual(r.context_data['object'], self.product)

    def test_non_members_cannot_update_product(self):
        """
        非メンバーはプロダクトを編集できない
        """
        login_url = settings.LOGIN_URL+'?next=/products/1/update/'
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.post('/products/1/update/', self.product_kwargs)
            self.assertRedirects(r, login_url)
            self.assertEqual(self.product.title, 'かわずたんのゲームだよ☆')

    def test_non_administrators_cannot_update_product(self):
        """
        非管理メンバーはプロダクトを編集できない
        """
        login_url = settings.LOGIN_URL+'?next=/products/1/update/'
        # adam は全ての権限を持つため除外
        for user in self.members[1:]:
            self.prefer_login(user)
            r = self.client.post('/products/1/update/', self.product_kwargs)
            self.assertRedirects(r, login_url)
            self.assertEqual(self.product.title, 'かわずたんのゲームだよ☆')

    def test_administrators_can_update_product(self):
        """
        管理メンバーはプロダクトを編集可能
        """
        for user in [self.members[0], self.administrator]:
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post('/products/1/update/',
                                     self.product_kwargs)
            self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=1)
            self.assertEqual(e.title, 'クラッカーだよ！！！')
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")

    def test_set_last_modifier_via_update_product(self):
        """
        プロダクト編集時にlast_modifierがセットされる
        """
        for user in [self.members[0], self.administrator]:
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post('/products/1/update/',
                                     self.product_kwargs)
            self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=1)
            self.assertEqual(e.last_modifier, user)

    def test_administrators_cannot_update_slug(self):
        """
        管理メンバーもスラグは編集不可
        """
        previous_slug = self.product.slug
        for user in [self.members[0], self.administrator]:
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                self.product_kwargs['slug'] = 'new-slug'
                r = self.client.post('/products/1/update/',
                                     self.product_kwargs)
            self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=1)
            self.assertEqual(e.title, 'クラッカーだよ！！！')
            self.assertEqual(e.slug, previous_slug)
            self.assertNotEqual(e.slug, 'new-slug')
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")


class ProductDeleteViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.administrator = PersonaFactory(username='administrator')
        self.product = ProductFactory(
            title="かわずたんのゲームだよ☆",
            administrators=(self.administrator,)
        )

    def test_non_members_cannot_delete_product(self):
        """
        非メンバーはプロダクトを削除できない
        """
        login_url = settings.LOGIN_URL+'?next=/products/1/delete/'
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.post('/products/1/delete/')
            self.assertRedirects(r, login_url)
            self.assertEqual(Product.objects.count(), 1)

    def test_non_administrators_cannot_delete_product(self):
        """
        非管理メンバーはプロダクトを削除できない
        """
        login_url = settings.LOGIN_URL+'?next=/products/1/delete/'
        # adam は全ての権限を持つため除外
        for user in self.members[1:]:
            self.prefer_login(user)
            r = self.client.post('/products/1/delete/')
            self.assertRedirects(r, login_url)
            self.assertEqual(Product.objects.count(), 1)

    def test_administrators_can_delete_product(self):
        """
        管理メンバーはプロダクトを削除可能
        """
        for i, user in enumerate([self.members[0], self.administrator]):
            self.prefer_login(user)
            r = self.client.post('/products/{}/delete/'.format(i+1))
            self.assertRedirects(r, '/products/')
            self.assertEqual(Product.objects.count(), 0)
            self.assertTrue('messages' in r.cookies,
                            "No messages are appeared")
            # 再作成
            self.product = ProductFactory(
                title="かわずたんのゲームだよ☆",
                administrators=(self.administrator,)
            )


class ProductPreviewTestCase(TestCase):
    def test_product_preview(self):
        """
        products_product_previewが表示できる
        """
        r = self.client.get('/products/preview/')
        self.assertTemplateUsed(r, 'products/components/product_detail.html')
        self.assertEqual(r.status_code, 200)
