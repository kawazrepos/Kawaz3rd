import os
import datetime
import itertools
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory

from ..models import Product
from .factories import ProductFactory
from .factories import PlatformFactory
from .factories import CategoryFactory


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
        product = ProductFactory(slug='kawaztan-adventure')
        for user in itertools.chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get('/products/kawaztan-adventure/')
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'products/product_detail.html')
            self.assertEqual(r.context['object'], product)


class ProductListViewTestCase(ViewTestCaseBase):
    def test_anyone_can_see_product_list(self):
        """
        プロダクトリストは誰でも閲覧可能
        """
        product = ProductFactory(slug='kawaztan-adventure')
        for user in itertools.chain(self.members, self.non_members):
            self.prefer_login(user)
            r = self.client.get('/products/')
            self.assertEqual(r.status_code, 200)
            self.assertTemplateUsed(r, 'products/product_list.html')
            self.assertTrue(product in r.context['object_list'])


class ProductCreateViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.product_kwargs = dict(
            title = 'かわずたんファンタジー',
            slug = 'kawaztan-fantasy',
            thumbnail = 'thumbnail.png',
            publish_at = datetime.date.today(),
            platforms = [1,],
            categories = [1,],
            description = '剣と魔法の物語です',
        )
        self.thumbnail_file = os.path.join(settings.REPOSITORY_ROOT,
                'src', 'kawaz', 'statics', 'fixtures', 'giginyan.png')

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

    def test_members_can_create_product(self):
        """
        メンバーはプロダクトを作成することが出来る
        """
        for user in self.members:
            self.prefer_login(user)
            with open(self.thumbnail_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post('/products/create/', self.product_kwargs)
            self.assertRedirects(r, '/products/kawaztan-fantasy/')
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=1)
            self.assertEqual(e.title, 'かわずたんファンタジー')
            self.assertTrue(user in e.administrators.all())
            self.assertEqual(e.administrators.count(), 1)
            # 重複を避けるため削除する
            e.delete()


class ProductUpdateViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.administrator = PersonaFactory(username='administrator')
        self.product = ProductFactory(title="かわずたんのゲームだよ☆",
                administrators=(self.administrator,))
        self.product_kwargs = dict(
            title = 'クラッカーだよ！！！',
            publish_at = datetime.date.today(),
            platforms = [1,],
            categories = [1,],
            description = '剣と魔法の物語です',
        )
        self.thumbnail_file = os.path.join(settings.REPOSITORY_ROOT,
                'src', 'kawaz', 'statics', 'fixtures', 'giginyan.png')

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
            with open(self.thumbnail_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                r = self.client.post('/products/1/update/', self.product_kwargs)
            self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=1)
            self.assertEqual(e.title, 'クラッカーだよ！！！')

    def test_administrators_cannot_update_slug(self):
        """
        管理メンバーもスラグは編集不可
        """
        previous_slug = self.product.slug
        for user in [self.members[0], self.administrator]:
            self.prefer_login(user)
            with open(self.thumbnail_file, 'rb') as f:
                self.product_kwargs['thumbnail'] = f
                self.product_kwargs['slug'] = 'new-slug'
                r = self.client.post('/products/1/update/', self.product_kwargs)
            self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
            self.assertEqual(Product.objects.count(), 1)
            e = Product.objects.get(pk=1)
            self.assertEqual(e.title, 'クラッカーだよ！！！')
            self.assertEqual(e.slug, previous_slug)
            self.assertNotEqual(e.slug, 'new-slug')


class ProductDeleteViewTestCase(ViewTestCaseBase):
    def setUp(self):
        super().setUp()
        self.administrator = PersonaFactory(username='administrator')
        self.product = ProductFactory(title="かわずたんのゲームだよ☆",
                administrators=(self.administrator,))

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
        for user in [self.members[0], self.administrator]:
            self.prefer_login(user)
            r = self.client.post('/products/1/delete/')
            self.assertRedirects(r, '/products/')
            self.assertEqual(Product.objects.count(), 0)
            # 再作成
            self.product = ProductFactory(title="かわずたんのゲームだよ☆",
                    administrators=(self.administrator,))

