from django.test import TestCase
from .factories import ProductFactory

class ProductDetailViewTestCase(TestCase):
    def test_anonymous_can_view_product_detail(self):
        """
        Tests anonymous user can view product detail view
        """
        product = ProductFactory(slug='kawaztan-adventure')
        r = self.client.get('/products/kawaztan-adventure/')
        self.assertTemplateUsed(r, 'products/product_detail.html')
        self.assertEqual(r.context['object'], product)

class ProductListViewTestCase(TestCase):
    pass

class ProductCreateViewTestCase(TestCase):
    pass