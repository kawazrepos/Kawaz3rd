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

    def test_other_user_dont_have_change_permission_with_object(self):
        '''
        Test other user don't have change product permission
        '''
        self.assertFalse(self.user.has_perm('products.change_product', self.product))

    def test_administrators_have_change_permission_with_object(self):
        '''
        Test administrators have change product permission
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

    def test_other_user_dont_have_delete_permission_with_object(self):
        '''
        Test other user don't have delete product permission
        '''
        self.assertFalse(self.user.has_perm('products.delete_product', self.product))

    def test_administrators_have_delete_permission_with_object(self):
        '''
        Test administrators have delete product permission
        '''
        self.product.administrators.add(self.user)
        self.assertTrue(self.user.has_perm('products.delete_product', self.product))

class ProductJoinPermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_join_permission(self):
        '''
        Test anonymous users do not have join to product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.join_product'))

    def test_wille_dont_have_join_permission(self):
        '''
        Test wille users do not have join to product permission
        '''
        self.assertFalse(self.wille.has_perm('products.join_product'))

    def test_general_user_have_join_permission(self):
        '''
        Test general user have join to product permission
        '''
        self.assertTrue(self.user.has_perm('products.join_product'))

    def test_anonymous_dont_have_join_permission_with_object(self):
        '''
        Test anonymous users do not have join to product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.join_product', self.product))

    def test_wille_dont_have_join_permission_with_object(self):
        '''
        Test wille users do not have join to product permission
        '''
        self.assertFalse(self.wille.has_perm('products.join_product', self.product))

    def test_other_user_have_join_permission_with_object(self):
        '''
        Test other user have join to product permission
        '''
        self.assertTrue(self.user.has_perm('products.join_product', self.product))

    def test_administrators_dont_have_join_permission_with_object(self):
        '''
        Test administrators don't have join to product permission
        '''
        self.product.administrators.add(self.user)
        self.assertFalse(self.user.has_perm('products.join_product', self.product))


class ProductQuitPermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_quit_permission(self):
        '''
        Test anonymous users do not have quit from product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.quit_product'))

    def test_wille_dont_have_quit_permission(self):
        '''
        Test wille users do not have quit from product permission
        '''
        self.assertFalse(self.wille.has_perm('products.quit_product'))

    def test_general_user_have_quit_permission(self):
        '''
        Test general user have quit from product permission
        '''
        self.assertTrue(self.user.has_perm('products.quit_product'))

    def test_anonymous_dont_have_quit_permission_with_object(self):
        '''
        Test anonymous users do not have quit from product permission
        '''
        self.assertFalse(self.anonymous.has_perm('products.quit_product', self.product))

    def test_wille_dont_have_quit_permission_with_object(self):
        '''
        Test wille users do not have quit from product permission
        '''
        self.assertFalse(self.wille.has_perm('products.quit_product', self.product))

    def test_other_user_dont_have_quit_permission_with_object(self):
        '''
        Test other user don't have quit from product permission
        '''
        self.assertFalse(self.user.has_perm('products.quit_product', self.product))

    def test_last_administrators_dont_have_quit_permission_with_object(self):
        '''
        Test last_administrators don't have quit from product permission
        '''
        self.product.administrators.add(self.user)
        self.assertEqual(self.product.administrators.count(), 1)
        self.assertFalse(self.user.has_perm('products.quit_product', self.product))

    def test_administrators_have_quit_permission_with_object(self):
        '''
        Test last_administrators have quit from product permission
        '''
        other = PersonaFactory()
        self.product.administrators.add(self.user)
        self.product.administrators.add(other)
        self.assertTrue(self.user.has_perm('products.quit_product', self.product))