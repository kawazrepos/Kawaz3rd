import os
import datetime
from itertools import chain
from contextlib import ExitStack
import tempfile
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Screenshot
from ..models import URLRelease
from ..models import PackageRelease

from ..models import Product
from .factories import ProductFactory, PackageReleaseFactory, URLReleaseFactory
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
    def test_reverse_product_detail_url(self):
        """
        ProductDetailViewの逆引き
        """
        product = ProductFactory(slug='super-kawaztan-adventure')
        self.assertEqual(
            reverse('products_product_detail', kwargs=dict(
                slug=product.slug,
            )),
            '/products/{}/'.format(product.slug),
        )

    def test_anyone_can_see_product_detail(self):
        """
        プロダクト詳細は誰でも閲覧可能
        """
        product = ProductFactory(slug='super-kawaztan-adventure')
        for user in chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get(product.get_absolute_url())
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

    def test_reverse_product_list_url(self):
        """
        ProductListViewの逆引き
        """
        self.assertEqual(
            reverse('products_product_list'),
            '/products/',
        )

    def test_anyone_can_see_product_list(self):
        """
        プロダクトリストは誰でも閲覧可能
        """
        product = ProductFactory()
        for user in chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get('/products/')
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'products/product_list.html')
            self.assertIn(product, r.context['filter'])

    def test_list_with_platforms(self):
        """
        プロダクトリストでPlatformのfilterが有効になっている
        """
        product1 = ProductFactory(platforms=(self.p0,))
        product2 = ProductFactory(platforms=(self.p1,))
        for user in chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get('/products/?platforms={}'.format(self.p0.pk))
            self.assertTemplateUsed(r, 'products/product_list.html')
            self.assertEqual(len(r.context['filter']), 1)
            self.assertIn(product1, r.context['filter'])
            self.assertNotIn(product2, r.context['filter'])

    def test_list_with_categories(self):
        """
        プロダクトリストでCategoryのfilterが有効になっている
        """
        product1 = ProductFactory(categories=(self.c0,))
        product2 = ProductFactory(categories=(self.c1,))
        self.prefer_login(self.members[0])
        r = self.client.get('/products/?categories={}'.format(self.c0.pk))
        self.assertTemplateUsed(r, 'products/product_list.html')
        self.assertEqual(len(r.context['filter']), 1)
        self.assertIn(product1, r.context['filter'])
        self.assertNotIn(product2, r.context['filter'])


class ProductCreateViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.platform = PlatformFactory()
        self.category = CategoryFactory()
        self.administrators = (
            PersonaFactory(),
            PersonaFactory(),
            PersonaFactory(),
        )
        self.product_kwargs = {
            'title': 'かわずたんファンタジー',
            'slug': 'kawaztan-fantasy',
            'thumbnail': 'thumbnail.png',
            'published_at': datetime.date.today(),
            'platforms': (self.platform.pk,),
            'categories': (self.category.pk,),
            'administrators': tuple(map(lambda x: x.pk, self.administrators)),
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

    def test_reverse_product_create_url(self):
        """
        ProductCreateViewの逆引き
        """
        self.assertEqual(
            reverse('products_product_create'),
            '/products/create/',
        )

    def test_non_members_cannot_see_create_view(self):
        """
        非メンバーはプロダクト作成画面に行けない
        """
        url = reverse('products_product_create')
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertRedirects(r, login_url)

    def test_members_can_see_create_view(self):
        """
        メンバーはプロダクト作成画面を見ることが出来る
        """
        url = reverse('products_product_create')
        for user in self.members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertTemplateUsed(r, 'products/product_form.html')
            self.assertNotIn('object', r.context_data)

    def test_non_members_cannot_create_product(self):
        """
        非メンバーはプロダクトの作成が出来ない
        """
        url = reverse('products_product_create')
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.post(url, self.product_kwargs)
            self.assertRedirects(r, login_url)

    def test_contact_info_initial_value(self):
        """
        Contact infoの初期値が
        ニックネーム: メールアドレス
        になっている
        """
        url = reverse('products_product_create')
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            r = self.client.get(url)
            form = r.context['form']
            contact_info = "{}: {}".format(user.nickname, user.email)
            self.assertEqual(form.fields['contact_info'].initial, contact_info)

    def test_members_can_create_product(self):
        """
        メンバーはプロダクトを作成することが出来る
        """
        url = reverse('products_product_create')
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post(url, self.product_kwargs)
            e = Product.objects.get(pk=i+1)
            self.assertRedirects(r, e.get_absolute_url())
            self.assertEqual(Product.objects.count(), 1)
            self.assertEqual(e.pk, i+1)
            self.assertEqual(e.title, 'かわずたんファンタジー')
            # administratorsに指定されたユーザーは管理者として登録されている
            administrators_qs = e.administrators.all()
            for administrator in self.administrators:
                self.assertIn(administrator, administrators_qs)
            # 作成者自身も管理者に追加される
            self.assertIn(user, administrators_qs)
            self.assertEqual(e.administrators.count(),
                             len(self.administrators) + 1)
            self.assertIn('messages', r.cookies, "No messages are appeared")
            # 重複を避けるため削除する
            e.delete()

    def test_set_last_modifier_via_create_view(self):
        """
        プロダクト作成時にlast_modifierが設定される
        """
        url = reverse('products_product_create')
        for i, user in enumerate(self.members):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post(url, self.product_kwargs)
            e = Product.objects.get(pk=i+1)
            self.assertRedirects(r, e.get_absolute_url())
            self.assertEqual(Product.objects.count(), 1)
            self.assertEqual(e.last_modifier, user)
            # 重複を避けるため削除する
            e.delete()

    def test_member_can_create_screenshot_via_product_form(self):
        """
        メンバーはプロダクトフォームからScreenshotモデルも作成できる
        """
        url = reverse('products_product_create')
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
                r = self.client.post(url, self.product_kwargs)
            e = Product.objects.get(pk=i+1)
            self.assertRedirects(r, e.get_absolute_url())
            self.assertEqual(Screenshot.objects.count(), 1)
            obj = Screenshot.objects.get(pk=i+1)
            self.assertIn('messages', r.cookies, "No messages are appeared")
            # 重複を避けるため削除する（プロダクトの削除も忘れずに）
            obj.product.delete()
            obj.delete()

    def test_member_can_create_url_release_via_product_form(self):
        """
        メンバーはプロダクトフォームからURLReleaseモデルも作成できる
        """
        url = reverse('products_product_create')
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
                r = self.client.post(url, self.product_kwargs)
            e = Product.objects.get(pk=i+1)
            self.assertRedirects(r, e.get_absolute_url())

            self.assertEqual(URLRelease.objects.count(), 1)
            obj = URLRelease.objects.get(pk=i+1)
            self.assertEqual(obj.label, 'Android版')
            self.assertEqual(obj.version, 'Version3.14')
            self.assertEqual(obj.platform, self.platform)
            self.assertIn('messages', r.cookies, "No messages are appeared")
            # 重複を避けるため削除する（プロダクトの削除も忘れずに）
            obj.product.delete()
            obj.delete()

    def test_member_can_create_package_release_via_product_form(self):
        """
        メンバーはプロダクトフォームからPackageReleaseモデルも作成できる
        """
        url = reverse('products_product_create')
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
                r = self.client.post(url, self.product_kwargs)
            e = Product.objects.get(pk=i+1)
            self.assertRedirects(r, e.get_absolute_url())

            self.assertEqual(PackageRelease.objects.count(), 1)
            obj = PackageRelease.objects.get(pk=i+1)
            self.assertEqual(obj.label, 'Android版')
            self.assertEqual(obj.version, 'Version3.14')
            self.assertEqual(obj.platform, self.platform)
            self.assertIn('messages', r.cookies, "No messages are appeared")
            # 重複を避けるため削除する（プロダクトの削除も忘れずに）
            obj.product.delete()
            obj.delete()


class ProductUpdateViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.platform = PlatformFactory()
        self.category = CategoryFactory()
        self.administrators = (
            PersonaFactory(),
            PersonaFactory(),
            PersonaFactory(),
        )
        self.product = ProductFactory(
            title="かわずたんのゲームだよ☆",
            administrators=tuple(map(lambda x: x.pk, self.administrators)),
        )
        self.product_kwargs = {
            'title': 'クラッカーだよ！！！',
            'published_at': datetime.date.today(),
            'platforms': (self.platform.pk,),
            'categories': (self.category.pk,),
            'administrators': tuple(map(lambda x: x.pk, self.administrators)),
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

    def test_reverse_product_update_url(self):
        """
        ProductUpdateViewの逆引き
        """
        self.assertEqual(
            reverse('products_product_update', kwargs=dict(
                slug=self.product.slug
            )),
            '/products/{}/update/'.format(self.product.slug),
        )

    def test_non_members_cannot_see_product_update_view(self):
        """
        非メンバーはプロダクト編集ページは見ることが出来ない
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertRedirects(r, login_url)

    def test_non_administrators_cannot_see_product_update_view(self):
        """
        非管理メンバーはプロダクト編集ページは見ることが出来ない
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        # adam は全ての権限を持つため除外
        for user in self.members[1:]:
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertRedirects(r, login_url)

    def test_administrators_can_view_product_update_view(self):
        """
        管理メンバーはプロダクト編集ページを見ることが出来る
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        # adam はすべての権限を持つため追加
        for user in chain([self.members[0]], self.administrators):
            self.prefer_login(user)
            r = self.client.get(url)
            self.assertTemplateUsed(r, 'products/product_form.html')
            self.assertIn('object', r.context_data)
            self.assertEqual(r.context_data['object'], self.product)

    def test_non_members_cannot_update_product(self):
        """
        非メンバーはプロダクトを編集できない
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.post(url, self.product_kwargs)
            self.assertRedirects(r, login_url)
            self.assertEqual(self.product.title, 'かわずたんのゲームだよ☆')

    def test_non_administrators_cannot_update_product(self):
        """
        非管理メンバーはプロダクトを編集できない
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        # adam は全ての権限を持つため除外
        for user in self.members[1:]:
            self.prefer_login(user)
            r = self.client.post(url, self.product_kwargs)
            self.assertRedirects(r, login_url)
            self.assertEqual(self.product.title, 'かわずたんのゲームだよ☆')

    def test_administrators_can_update_product(self):
        """
        管理メンバーはプロダクトを編集可能
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        # adam はすべての権限を持つため追加
        for user in chain([self.members[0]], self.administrators):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post(url, self.product_kwargs)
            self.assertRedirects(r, self.product.get_absolute_url())
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=self.product.pk)
            self.assertEqual(e.title, 'クラッカーだよ！！！')
            self.assertIn('messages', r.cookies, "No messages are appeared")

    def test_set_last_modifier_via_update_product(self):
        """
        プロダクト編集時にlast_modifierがセットされる
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        # adam はすべての権限を持つため追加
        for user in chain([self.members[0]], self.administrators):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post(url, self.product_kwargs)
            self.assertRedirects(r, self.product.get_absolute_url())
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=self.product.pk)
            self.assertEqual(e.last_modifier, user)

    def test_administrators_cannot_update_slug(self):
        """
        管理メンバーもスラグは編集不可
        """
        url = reverse('products_product_update', kwargs=dict(
            slug=self.product.slug,
        ))
        previous_slug = self.product.slug
        # adam はすべての権限を持つため追加
        for user in chain([self.members[0]], self.administrators):
            self.prefer_login(user)
            with open(self.image_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                self.product_kwargs['slug'] = 'new-slug'
                r = self.client.post(url, self.product_kwargs)
            self.assertRedirects(r, self.product.get_absolute_url())
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=self.product.pk)
            self.assertEqual(e.title, 'クラッカーだよ！！！')
            self.assertEqual(e.slug, previous_slug)
            self.assertNotEqual(e.slug, 'new-slug')
            self.assertIn('messages', r.cookies, "No messages are appeared")


class ProductDeleteViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.administrator = PersonaFactory(username='administrator')
        self.product = ProductFactory(
            title="かわずたんのゲームだよ☆",
            administrators=(self.administrator,)
        )

    def test_reverse_product_delete_url(self):
        """
        ProductDeleteViewの逆引き
        """
        self.assertEqual(
            reverse('products_product_delete', kwargs=dict(
                slug=self.product.slug
            )),
            '/products/{}/delete/'.format(self.product.slug),
        )

    def test_non_members_cannot_delete_product(self):
        """
        非メンバーはプロダクトを削除できない
        """
        url = reverse('products_product_delete', kwargs=dict(
            slug=self.product.slug,
        ))
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        for user in self.non_members:
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertRedirects(r, login_url)
            self.assertEqual(Product.objects.count(), 1)

    def test_non_administrators_cannot_delete_product(self):
        """
        非管理メンバーはプロダクトを削除できない
        """
        url = reverse('products_product_delete', kwargs=dict(
            slug=self.product.slug,
        ))
        login_url = "{}?next={}".format(settings.LOGIN_URL, url)
        # adam は全ての権限を持つため除外
        for user in self.members[1:]:
            self.prefer_login(user)
            r = self.client.post(url)
            self.assertRedirects(r, login_url)
            self.assertEqual(Product.objects.count(), 1)

    def test_administrators_can_delete_product(self):
        """
        管理メンバーはプロダクトを削除可能
        """
        # adamはすべての権限を持つため追加
        for i, user in enumerate([self.members[0], self.administrator]):
            self.prefer_login(user)
            url = reverse('products_product_delete', kwargs=dict(
                slug=self.product.slug,
            ))
            r = self.client.post(url)
            self.assertRedirects(r, '/products/')
            self.assertEqual(Product.objects.count(), 0)
            self.assertIn('messages', r.cookies, "No messages are appeared")
            # 再作成
            self.product = ProductFactory(
                title="かわずたんのゲームだよ☆",
                administrators=(self.administrator,)
            )


class ProductPreviewTestCase(TestCase):
    def test_reverse_product_preview_url(self):
        """
        ProductPreviewViewの逆引き
        """
        self.assertEqual(
            reverse('products_product_preview'),
            '/products/preview/',
        )

    def test_product_preview(self):
        """
        products_product_previewが表示できる
        """
        import json
        url = reverse('products_product_preview')
        r = self.client.post(url, json.dumps({}),
                             content_type='application/json')
        self.assertTemplateUsed(r, 'products/components/product_detail.html')
        self.assertEqual(r.status_code, 200)


class PackageReleaseDetailViewTestCase(TestCase):
    def _generate_package_release(self, ext=''):
        """
        拡張子がextの一時ファイルを持ったPackageReleaseを生成します
        """
        slug = "hogehoge"
        path = os.path.join(settings.MEDIA_ROOT, 'products', slug, 'releases')
        if not os.path.exists(path):
            os.makedirs(path)
        tmp_file = tempfile.mkstemp(dir=path, suffix=ext)[1]
        name = os.path.split(tmp_file)[-1]
        release = PackageReleaseFactory(file_content=name, product__slug=slug)
        self.assertTrue(os.path.exists(release.file_content.path))
        return release

    def test_reverse_package_release_detail_url(self):
        """
        PackageReleaseDetailViewの逆引き
        """
        release = self._generate_package_release()
        self.assertEqual(
            reverse('products_package_release_detail', kwargs=dict(
                pk=release.pk,
            )),
            '/products/package_releases/{}/'.format(release.pk),
        )

    def test_package_release_detail_view(self):
        """
        PackageDetailViewにアクセスしてファイルをダウンロードできる
        また、downloadsカウントが+1される
        """
        release = self._generate_package_release()
        # ダウンロードカウントが0
        self.assertEqual(release.downloads, 0)
        r = self.client.get(release.get_absolute_url())

        # Content-Dispositionの値が正しい
        self.assertEqual(r['Content-Disposition'],
                         'attachment; filename={}'.format(release.filename))

        # ダウンロードカウントが1
        release = PackageRelease.objects.get(pk=release.pk)
        self.assertEqual(release.downloads, 1)


class URLReleaseDetailView(TestCase):

    def test_reverse_url_release_detail_url(self):
        """
        URLReleaseDetailViewの逆引き
        """
        release = URLReleaseFactory() 
        self.assertEqual(
            reverse('products_url_release_detail', kwargs=dict(
                pk=release.pk,
            )),
            '/products/url_releases/{}/'.format(release.pk),
        )

    def test_url_release_detail_view(self):
        """
        URLReleaseDetailViewにアクセスしてURLにリダイレクトできる
        また、pageviewが+1される
        """
        release = URLReleaseFactory()
        # ページビューが0
        self.assertEqual(release.pageview, 0)

        r = self.client.get(release.get_absolute_url())
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['Location'], release.url)

        # ページビューが1
        release = URLRelease.objects.get(pk=release.pk)
        self.assertEqual(release.pageview, 1)
