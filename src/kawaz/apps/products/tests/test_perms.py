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