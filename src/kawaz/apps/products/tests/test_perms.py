from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import ProductFactory

class ProductCreatePermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_add_permission(self):
        '''
        Test anonymous users do not have add product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.add_product'))

    def test_wille_dont_have_add_permission(self):
        '''
        Test wille users do not have add product permission
        '''
        self.assertFalse(self.wille.has_perm('products.add_product'))

    def test_general_user_have_add_permission(self):
        '''
        Test general user have add product permission
        '''
        self.assertTrue(self.user.has_perm('products.add_product'))

class ProductUpdatePermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_change_permission(self):
        '''
        Test anonymous users do not have change product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.change_product'))

    def test_wille_dont_have_change_permission(self):
        '''
        Test wille users do not have change product permission
        '''
        self.assertFalse(self.wille.has_perm('products.change_product'))

    def test_general_user_have_change_permission(self):
        '''
        Test general user have change product permission
        '''
        self.assertTrue(self.user.has_perm('products.change_product'))

    def test_anonymous_dont_have_change_permission_with_object(self):
        '''
        Test anonymous users do not have change product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.change_product', self.product))

    def test_wille_dont_have_change_permission_with_object(self):
        '''
        Test wille users do not have change product permission
        '''
        self.assertFalse(self.wille.has_perm('products.change_product', self.product))

    def test_other_user_have_change_permission_with_object(self):
        '''
        Test other user don't have change product permission
        '''
        self.assertFalse(self.user.has_perm('products.change_product', self.product))

    def test_administrators_have_change_permission_with_object(self):
        '''
        Test administrators don't have change product permission
        '''
        self.product.administrators.add(self.user)
        self.assertTrue(self.user.has_perm('products.change_product', self.product))

class ProductDeletePermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_delete_permission(self):
        '''
        Test anonymous users do not have delete product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.delete_product'))

    def test_wille_dont_have_delete_permission(self):
        '''
        Test wille users do not have delete product permission
        '''
        self.assertFalse(self.wille.has_perm('products.delete_product'))

    def test_general_user_have_delete_permission(self):
        '''
        Test general user have delete product permission
        '''
        self.assertTrue(self.user.has_perm('products.delete_product'))

    def test_anonymous_dont_have_delete_permission_with_object(self):
        '''
        Test anonymous users do not have delete product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.delete_product', self.product))

    def test_wille_dont_have_delete_permission_with_object(self):
        '''
        Test wille users do not have delete product permission
        '''
        self.assertFalse(self.wille.has_perm('products.delete_product', self.product))

    def test_other_user_have_delete_permission_with_object(self):
        '''
        Test other user don't have delete product permission
        '''
        self.assertFalse(self.user.has_perm('products.delete_product', self.product))

    def test_administrators_have_delete_permission_with_object(self):
        '''
        Test administrators don't have delete product permission
        '''
        self.product.administrators.add(self.user)
        self.assertTrue(self.user.has_perm('products.delete_product', self.product))