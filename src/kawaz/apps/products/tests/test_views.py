from django.test import TestCase
from django.conf import settings
from ..models import Product
from .factories import ProductFactory
from .factories import PlatformFactory
from .factories import CategoryFactory
from kawaz.core.personas.tests.factories import PersonaFactory

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
    def test_anonymous_can_view_product_list(self):
        """
        Tests anonymous user can view product list view
        """
        product = ProductFactory(slug='kawaztan-adventure')
        r = self.client.get('/products/')
        self.assertTemplateUsed(r, 'products/product_list.html')
        self.assertIsNotNone(r.context['object_list'])
        self.assertTrue(product in r.context['object_list'])

class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.platform = PlatformFactory()
        self.category = CategoryFactory()

    def test_anonymous_user_can_not_create_view(self):
        '''Tests anonymous user can not view ProductCreateView'''
        r = self.client.get('/products/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/create/')

    def test_wille_user_can_not_view_product_create_view(self):
        '''Tests wille user can not view ProductCreateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/products/create/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/create/')

    def test_authorized_user_can_view_product_create_view(self):
        '''Tests authorized user can view ProductCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/products/create/')
        self.assertTemplateUsed(r, 'products/product_form.html')
        self.assertFalse('object' in r.context_data)

    def test_anonymous_user_can_not_create_via_create_view(self):
        '''Tests anonymous user can not create product via ProductCreateView'''
        r = self.client.post('/products/create/', {
            'title' : 'かわずたんファンタジー',
            'slug' : 'kawaztan-fantasy',
            'platforms' : [1,],
            'categories' : [1,],
            'description' : '剣と魔法の物語です',
            'display_mode' : 3
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/create/')

    def test_wille_user_can_not_create_via_create_view(self):
        '''Tests wille user can not create product via ProductCreateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/products/create/', {
            'title' : 'かわずたんファンタジー',
            'slug' : 'kawaztan-fantasy',
            'platforms' : [1,],
            'categories' : [1,],
            'description' : '剣と魔法の物語です',
            'display_mode' : 3
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/create/')

    def test_authorized_user_can_create_via_create_view(self):
        '''Tests authorized user can create product via ProductCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/products/create/', {
            'title' : 'かわずたんファンタジー',
            'slug' : 'kawaztan-fantasy',
            'platforms' : [1,],
            'categories' : [1,],
            'description' : '剣と魔法の物語です',
            'display_mode' : 3
        })
        self.assertRedirects(r, '/products/kawaztan-fantasy/')
        self.assertEqual(Product.objects.count(), 1)
        e = Product.objects.get(pk=1)
        self.assertEqual(e.title, 'かわずたんファンタジー')

    def test_user_cannot_modify_administrators_id(self):
        '''
        Tests authorized user cannot modify administrators id.
        In product creation form, `administrators` is exist as hidden field.
        So user can modify `administrators` to invalid values.
        This test checks that `administrators` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/products/create/', {
            'title' : 'かわずたんファンタジー',
            'slug' : 'kawaztan-fantasy',
            'platforms' : [1,],
            'categories' : [1,],
            'description' : '剣と魔法の物語です',
            'display_mode' : 3,
            'administrators' : [other.pk,] # cracker attempt to masquerade
        })
        self.assertRedirects(r, '/products/kawaztan-fantasy/')
        self.assertEqual(Product.objects.count(), 1)
        e = Product.objects.get(pk=1)
        self.assertTrue(self.user in e.administrators.all())
        self.assertFalse(other in e.administrators.all())


class ProductUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='administrator_kawaztan')
        self.user.set_password('password')
        self.other = PersonaFactory(username='black_kawaztan')
        self.other.set_password('password')
        self.user.save()
        self.other.save()
        self.product = ProductFactory(title='かわずたんのゲームだよ☆', administrator=self.user)
        self.category = CategoryFactory()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_anonymous_user_can_not_view_product_update_view(self):
        '''Tests anonymous user can not view ProductUpdateView'''
        r = self.client.get('/products/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/1/update/')

    def test_wille_user_can_not_view_product_update_view(self):
        '''Tests wille user can not view ProductUpdateView'''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/products/1/update/')
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/1/update/')

    def test_authorized_user_can_view_product_update_view(self):
        '''
        Tests authorized user can view ProductUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/products/1/update/')
        self.assertTemplateUsed(r, 'products/product_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.product)

    def test_member_can_view_product_update_view(self):
        '''
        Tests product members can view ProductUpdateView
        '''
        self.product.join(self.other)
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.get('/products/1/update/')
        self.assertTemplateUsed(r, 'products/product_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.product)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update product via ProductUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/products/1/update/', {
            'pub_state' : 'public',
            'title' : 'クラッカーだよー',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/1/update/')
        self.assertEqual(self.product.title, 'かわずたんのゲームだよ☆')

    def test_wille_user_can_not_update_via_update_view(self):
        '''
        Tests wille user can not update product via ProductUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/products/1/update/', {
            'pub_state' : 'public',
            'title' : '外部ユーザーだよーん',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/1/update/')
        self.assertEqual(self.product.title, 'かわずたんのゲームだよ☆')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update product via ProductUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/products/1/update/', {
            'pub_state' : 'public',
            'title' : 'いたずら日記です',
            'body' : '黒かわずたんだよーん',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/products/1/update/')
        self.assertEqual(self.product.title, 'かわずたんのゲームだよ☆')

    def test_administrator_can_update_via_update_view(self):
        '''Tests administrator user can update product via ProductUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/products/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
        self.assertEqual(Product.objects.count(), 1)
        e = Product.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')

    def test_member_can_update_via_update_view(self):
        '''Tests product member can update product via ProductUpdateView'''
        self.product.join(self.other)
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/products/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk
        })
        self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
        self.assertEqual(Product.objects.count(), 1)
        e = Product.objects.get(pk=1)
        self.assertEqual(e.title, 'やっぱり書き換えます！')

    def test_user_cannot_update_slug(self):
        '''Tests anyone cannot update prject's slug'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        old_slug = self.product.slug
        r = self.client.post('/products/1/update/', {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk,
            'slug' : 'new-slug'
        })
        self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
        self.assertEqual(Product.objects.count(), 1)
        e = Product.objects.get(pk=1)
        self.assertEqual(e.slug, old_slug)
        self.assertNotEqual(e.slug, 'new-slug')

    def test_user_cannot_modify_administrator_id(self):
        '''
        Tests authorized user cannot modify administrator id.
        In product update form, `administrator` is exist as hidden field.
        So user can modify `administrator` to invalid values.
        This test checks that `administrator` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/products/1/update/', {
            'pub_state' : 'public',
            'title' : 'ID書き換えます！',
            'body' : 'うえーい',
            'status' : 'planning',
            'category' : self.category.pk,
            'administrator' : other.pk # crackers attempt to masquerade
        })
        self.assertRedirects(r, '/products/{}/'.format(self.product.slug))
        self.assertEqual(Product.objects.count(), 1)
        e = Product.objects.get(pk=1)
        self.assertEqual(e.administrator, self.user)
        self.assertNotEqual(e.administrator, other)
        self.assertEqual(e.title, 'ID書き換えます！')

class ProductDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()
        self.other = PersonaFactory()
        self.other.set_password('password')
        self.other.save()
        self.product = ProductFactory(administrator=self.user)

    def test_administrator_can_delete_via_product_delete_view(self):
        '''
        Tests administrators can delete its own products via ProductDeleteView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/products/1/delete/', {})
        self.assertEqual(Product.objects.count(), 0)

    def test_member_cannot_delete_via_product_delete_view(self):
        '''
        Tests members cannot delete its products via ProductDeleteView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        self.product.join(self.other)
        r = self.client.post('/products/1/delete/', {})
        self.assertEqual(Product.objects.count(), 1)

    def test_other_cannot_delete_via_product_delete_view(self):
        '''
        Tests others cannot delete products via ProductDeleteView
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/products/1/delete/', {})
        self.assertEqual(Product.objects.count(), 1)

    def test_wille_cannot_delete_via_product_delete_view(self):
        '''
        Tests wille cannot delete products via ProductDeleteView
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.post('/products/1/delete/', {})
        self.assertEqual(Product.objects.count(), 1)

    def test_anonymous_cannot_delete_via_product_delete_view(self):
        '''
        Tests anonymous cannot delete products via ProductDeleteView
        '''
        r = self.client.post('/products/1/delete/', {})
        self.assertEqual(Product.objects.count(), 1)
