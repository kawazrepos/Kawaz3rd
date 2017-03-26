from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory
from django.template import Template, Context, TemplateSyntaxError
from django.conf import settings
from unittest.mock import MagicMock
from kawaz.core.personas.tests.utils import create_role_users
from ..models import Category
from .factories import ProductFactory, URLReleaseFactory
from .factories import PlatformFactory
from .factories import CategoryFactory


class ProductsTemplateTagTestCase(TestCase):
    def setUp(self):
        self.users = create_role_users()
        self.products = (
            ProductFactory(display_mode='normal'),
            ProductFactory(display_mode='normal'),
            ProductFactory(display_mode='normal'),
            ProductFactory(display_mode='featured'),
            ProductFactory(display_mode='featured'),
            ProductFactory(display_mode='tiled'),
        )

    def _render_template(self, username, lookup=''):
        t = Template(
            "{{% load products_tags %}}"
            "{{% get_products {} as products %}}".format(
                "'{}'".format(lookup) if lookup else ''
            )
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r))
        r = t.render(c)
        # get_blog_products は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['products']

    def test_get_products_mixed(self):
        """get_products mixed は display_mode が featured/tiled なものを返す"""
        patterns = (
            ('adam', 3),
            ('seele', 3),
            ('nerv', 3),
            ('children', 3),
            ('wille', 3),
            ('anonymous', 3),
        )
        # with lookup
        for username, nproducts in patterns:
            products = self._render_template(username, lookup='mixed')
            self.assertEqual(products.count(), nproducts,
                             "{} should see {} products.".format(username,
                                                                 nproducts))
        # without lookup
        for username, nproducts in patterns:
            products = self._render_template(username)
            self.assertEqual(products.count(), nproducts,
                             "{} should see {} products.".format(username,
                                                                 nproducts))

    def test_get_products_normal(self):
        """get_products normal は display_mode が normal なものを返す"""
        patterns = (
            ('adam', 3),
            ('seele', 3),
            ('nerv', 3),
            ('children', 3),
            ('wille', 3),
            ('anonymous', 3),
        )
        # with lookup
        for username, nproducts in patterns:
            products = self._render_template(username, lookup='normal')
            self.assertEqual(products.count(), nproducts,
                             "{} should see {} products.".format(username,
                                                                 nproducts))

    def test_get_products_featured(self):
        """get_products featured は display_mode が featured なものを返す"""
        patterns = (
            ('adam', 2),
            ('seele', 2),
            ('nerv', 2),
            ('children', 2),
            ('wille', 2),
            ('anonymous', 2),
        )
        # with lookup
        for username, nproducts in patterns:
            products = self._render_template(username, lookup='featured')
            self.assertEqual(products.count(), nproducts,
                             "{} should see {} products.".format(username,
                                                                 nproducts))

    def test_get_products_tiled(self):
        """get_products featured は display_mode が tiled なものを返す"""
        patterns = (
            ('adam', 1),
            ('seele', 1),
            ('nerv', 1),
            ('children', 1),
            ('wille', 1),
            ('anonymous', 1),
        )
        # with lookup
        for username, nproducts in patterns:
            products = self._render_template(username, lookup='tiled')
            self.assertEqual(products.count(), nproducts,
                             "{} should see {} products.".format(username,
                                                                 nproducts))

    def test_get_products_unknown(self):
        """get_products unknown はエラーを出す"""
        patterns = (
            ('adam', 0),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
        )
        # with lookup
        for username, nproducts in patterns:
            self.assertRaises(TemplateSyntaxError, self._render_template,
                              username, lookup='unknown')


class GetProductsByCategoriesTestCase(TestCase):
    def _render_template(self, categories):
        t = Template(
            "{% load products_tags %}"
            "{% get_products_by_categories categories as products %}"
        )
        c = Context({'categories': categories})
        r = t.render(c)
        # get_blog_products は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['products']

    def test_get_products_by_categories(self):
        """
        get_products_by_categoriesで指定したカテゴリを含むQuerySetを返せる
        """
        c0 = CategoryFactory(label="バカゲー")
        c1 = CategoryFactory(label="クソゲー")
        p0 = ProductFactory(categories=(c0,))
        p1 = ProductFactory(categories=(c1,))
        p2 = ProductFactory(categories=[c0, c1])

        categories0 = Category.objects.filter(pk__in=(c0.pk,))
        products0 = self._render_template(categories=categories0)
        self.assertEqual(len(products0), 2)
        self.assertEqual(products0[0], p0)
        self.assertEqual(products0[1], p2)
        categories1 = Category.objects.filter(pk__in=(c1.pk,))
        products1 = self._render_template(categories=categories1)
        self.assertEqual(products1[0], p1)
        self.assertEqual(products1[1], p2)
        self.assertEqual(len(products1), 2)
        categories2 = Category.objects.filter(pk__in=(c0.pk, c1.pk))
        products2 = self._render_template(categories=categories2)
        self.assertEqual(len(products2), 3)
        self.assertEqual(products2[0], p0)
        self.assertEqual(products2[1], p2)
        self.assertEqual(products2[2], p1)


class GetRelativeTestCase(TestCase):
    def _render_template(self, product):
        t = Template(
            "{% load products_tags %}"
            "{% get_relative product as products %}"
        )
        c = Context({'product': product})
        r = t.render(c)
        # get_relative_products は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['products']

    def test_get_relative(self):
        """
        get_relativeで指定したカテゴリを含むQuerySetが返る
        """
        c0 = CategoryFactory(label="バカゲー")
        c1 = CategoryFactory(label="クソゲー")
        p0 = ProductFactory(categories=(c0,))
        p1 = ProductFactory(categories=(c0,))
        p2 = ProductFactory(categories=(c1,))
        p3 = ProductFactory(categories=(c0, c1))

        products = self._render_template(p0)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0], p1)
        self.assertEqual(products[1], p3)
        products = self._render_template(p1)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0], p0)
        self.assertEqual(products[1], p3)
        products = self._render_template(p2)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0], p3)
        products = self._render_template(p3)
        self.assertEqual(len(products), 3)
        self.assertEqual(products[0], p0)
        self.assertEqual(products[1], p1)
        self.assertEqual(products[2], p2)


class GetPlatformsTestCase(TestCase):
    def _render_template(self):
        t = Template(
            "{% load products_tags %}"
            "{% get_platforms as platforms %}"
        )
        c = Context()
        r = t.render(c)
        # get_platforms は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['platforms']

    def test_get_platforms(self):
        """
        get_platformsで全てのPlatformを含むQuerySetを返す
        """
        PlatformFactory(label='OUYA')
        PlatformFactory(label='GameStick')
        PlatformFactory(label='Fire TV')
        platforms = self._render_template()
        self.assertEqual(len(platforms), 3)


class GetCategoriesTestCase(TestCase):
    def _render_template(self):
        t = Template(
            "{% load products_tags %}"
            "{% get_categories as categories %}"
        )
        c = Context()
        r = t.render(c)
        # get_categories は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['categories']

    def test_get_categories(self):
        """
        get_categoriesで全てのCategoryを含むQuerySetを返す
        """
        CategoryFactory(label="泣きゲー")
        CategoryFactory(label="神ゲー")
        CategoryFactory(label="スルメゲー")
        categories = self._render_template()
        self.assertEqual(len(categories), 3)

class RenderTwitterCardTestCase(TestCase):
    def _render_template(self, product):
        t = Template(
            "{% load products_tags %}"
            "{% render_twitter_card product %}"
        )
        c = Context({
            'product': product
        })
        r = t.render(c)
        return r

    def test_render_twitter_card(self):
        """
        {% render_twitter_card product %}でproducts/components/twitter_card.htmlが描画できる
        """
        product = ProductFactory()
        ios_app = URLReleaseFactory(product=product, url="https://itunes.apple.com/ja/app/kawazutanjetto!/id922471335?mt=8")
        google_app = URLReleaseFactory(product=product, url="https://play.google.com/store/apps/details?id=org.kawaz.KawazJet")
        other_app = URLReleaseFactory(product=product, url="http://www.google.com/")

        apps = [ios_app, google_app]
        c = Context({
            'apps': apps,
            'product': product,
            'MEDIA_URL': settings.MEDIA_URL
        })
        expect = render_to_string('products/components/twitter_card.html', c)
        rendered = self._render_template(product)
        self.assertEqual(rendered, expect)

