from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.personas.tests.utils import create_role_users
from ..models import Category
from ..models import Product
from .factories import ProductFactory
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
        """
        """
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
        p0 = ProductFactory(categories=[c0,])
        p1 = ProductFactory(categories=[c1,])
        p2 = ProductFactory(categories=[c0, c1])

        categories0 = Category.objects.filter(pk__in=[1,])
        products0 = self._render_template(categories=categories0)
        self.assertEqual(len(products0), 2)
        self.assertEqual(products0[0], p0)
        self.assertEqual(products0[1], p2)
        categories1 = Category.objects.filter(pk__in=[2,])
        products1 = self._render_template(categories=categories1)
        self.assertEqual(products1[0], p1)
        self.assertEqual(products1[1], p2)
        self.assertEqual(len(products1), 2)
        categories2 = Category.objects.filter(pk__in=[1, 2])
        products2 = self._render_template(categories=categories2)
        self.assertEqual(len(products2), 3)
        self.assertEqual(products2[0], p0)
        self.assertEqual(products2[1], p2)
        self.assertEqual(products2[2], p1)
