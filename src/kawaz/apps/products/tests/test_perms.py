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
        """
        非ログインユーザーはプロダクト作成権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.add_product'))

    def test_wille_dont_have_add_permission(self):
        """
        Willeユーザーはプロダクト作成権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.add_product'))

    def test_general_user_have_add_permission(self):
        """
        通常ユーザーはプロダクト作成権限を持つ
        """
        self.assertTrue(self.user.has_perm('products.add_product'))


class ProductUpdatePermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_change_permission(self):
        """
        非ログインユーザーはプロダクト編集権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.change_product'))

    def test_wille_dont_have_change_permission(self):
        """
        Willeユーザーはプロダクト編集権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.change_product'))

    def test_general_user_have_change_permission(self):
        """
        通常ユーザーはプロダクト編集権限を持つ
        """
        self.assertTrue(self.user.has_perm('products.change_product'))

    def test_anonymous_dont_have_change_permission_with_object(self):
        """
        非ログインユーザーは特定のプロダクトに対する編集権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.change_product',
                                                 self.product))

    def test_wille_dont_have_change_permission_with_object(self):
        """
        Willeユーザーは特定のプロダクトに対する編集権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.change_product',
                                             self.product))

    def test_other_user_dont_have_change_permission_with_object(self):
        """
        通常ユーザーは特定のプロダクトに対する編集権限を持たない
        """
        self.assertFalse(self.user.has_perm('products.change_product',
                                            self.product))

    def test_administrators_have_change_permission_with_object(self):
        """
        管理者は自身が管理する特定のプロダクトに対する編集権限を持つ
        """
        self.product.administrators.add(self.user)
        self.assertTrue(self.user.has_perm('products.change_product',
                                           self.product))


class ProductDeletePermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_delete_permission(self):
        """
        非ログインユーザーはプロダクト削除権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.delete_product'))

    def test_wille_dont_have_delete_permission(self):
        """
        Willeユーザーはプロダクト削除権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.delete_product'))

    def test_general_user_have_delete_permission(self):
        """
        通常ユーザーはプロダクト削除権限を持つ
        """
        self.assertTrue(self.user.has_perm('products.delete_product'))

    def test_anonymous_dont_have_delete_permission_with_object(self):
        """
        非ログインユーザーは特定プロダクトに対する削除権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.delete_product',
                                                 self.product))

    def test_wille_dont_have_delete_permission_with_object(self):
        """
        Willeユーザーは特定プロダクトに対する削除権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.delete_product',
                                             self.product))

    def test_other_user_dont_have_delete_permission_with_object(self):
        """
        通常ユーザーは特定プロダクトに対する削除権限を持たない
        """
        self.assertFalse(self.user.has_perm('products.delete_product',
                                            self.product))

    def test_administrators_have_delete_permission_with_object(self):
        """
        管理者は自身が管理する特定プロダクトに対する削除権限を持つ
        """
        self.product.administrators.add(self.user)
        self.assertTrue(self.user.has_perm('products.delete_product',
                                           self.product))


class ProductJoinPermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_join_permission(self):
        """
        非ログインユーザーはプロダクト参加権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.join_product'))

    def test_wille_dont_have_join_permission(self):
        """
        Willeユーザーはプロダクト参加権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.join_product'))

    def test_general_user_have_join_permission(self):
        """
        通常ユーザーはプロダクト参加権限を持つ
        """
        self.assertTrue(self.user.has_perm('products.join_product'))

    def test_anonymous_dont_have_join_permission_with_object(self):
        """
        非ログインユーザーは特定のプロダクトに対する参加権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.join_product',
                                                 self.product))

    def test_wille_dont_have_join_permission_with_object(self):
        """
        Willeユーザーは特定のプロダクトに対する参加権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.join_product',
                                             self.product))

    def test_other_user_have_join_permission_with_object(self):
        """
        通常ユーザーは特定のプロダクトに対する参加権限を持つ
        """
        self.assertTrue(self.user.has_perm('products.join_product',
                                           self.product))

    def test_administrators_dont_have_join_permission_with_object(self):
        """
        管理者は自身が管理する特定のプロダクトに対する参加権限を持たない
        """
        self.product.administrators.add(self.user)
        self.assertFalse(self.user.has_perm('products.join_product',
                                            self.product))


class ProductQuitPermissionTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.anonymous = AnonymousUser()

    def test_anonymous_dont_have_quit_permission(self):
        """
        非ログインユーザーはプロダクト不参加権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.quit_product'))

    def test_wille_dont_have_quit_permission(self):
        """
        Willeユーザーはプロダクト不参加権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.quit_product'))

    def test_general_user_have_quit_permission(self):
        """
        通常ユーザーはプロダクト不参加権限を持つ
        """
        self.assertTrue(self.user.has_perm('products.quit_product'))

    def test_anonymous_dont_have_quit_permission_with_object(self):
        """
        非ログインユーザーは特定のプロダクトに対する不参加権限を持たない
        """
        self.assertFalse(self.anonymous.has_perm('products.quit_product',
                                                 self.product))

    def test_wille_dont_have_quit_permission_with_object(self):
        """
        Willeユーザーは特定のプロダクトに対する不参加権限を持たない
        """
        self.assertFalse(self.wille.has_perm('products.quit_product',
                                             self.product))

    def test_other_user_dont_have_quit_permission_with_object(self):
        """
        通常ユーザーは特定のプロダクトに対する不参加権限を持たない
        """
        self.assertFalse(self.user.has_perm('products.quit_product',
                                            self.product))

    def test_administrators_have_quit_permission_with_object(self):
        """
        管理者は管理しているプロダクトに対する不参加資格を持つ
        """
        other = PersonaFactory()
        self.product.administrators.add(self.user)
        self.product.administrators.add(other)
        self.assertTrue(self.user.has_perm('products.quit_product',
                                           self.product))

    def test_last_administrators_dont_have_quit_permission_with_object(self):
        """
        管理者は管理しているプロダクトに他に管理者がいない場合は不参加資格を
        持たない（管理者不在になるため）
        """
        self.product.administrators.add(self.user)
        self.assertEqual(self.product.administrators.count(), 1)
        self.assertFalse(self.user.has_perm('products.quit_product',
                                            self.product))
