from kawaz.apps.projects.tests.factories import ProjectFactory
from kawaz.core.personas.models import Persona
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.tests.testcases.permissions import BasePermissionLogicTestCase
from .factories import ProductFactory


class ProductPermissionLogicTestCase(BasePermissionLogicTestCase):
    app_label = 'products'
    model_name = 'product'

    def setUp(self):
        super().setUp()
        self.users['administrator'] = PersonaFactory(
            username='administrator',
            role='children'
        )
        self.users['project_member'] = PersonaFactory(
            username='project_member',
            role='children'
        )
        self.project = ProjectFactory()
        self.project.join(self.users['project_member'])
        self.product = ProductFactory(project=self.project)
        # Note:
        #   self.product.join で加えても良いが、内部で user.has_perm を呼ぶ
        #   ので django-permission により結果がキャッシュされ、今後のテスト
        #   結果に影響するため、直接 administrators.add を呼び出している
        self.product.administrators.add(self.users['administrator'])

    def test_add_permission(self):
        """
        ログインユーザー以上にモデルの追加権限がある
        """
        self._test('adam', 'add')
        self._test('seele', 'add')
        self._test('nerv', 'add')
        self._test('children', 'add')
        self._test('wille', 'add', neg=True)
        self._test('anonymous', 'add', neg=True)
        self._test('administrator', 'add')
        self._test('project_member', 'add')

    def test_change_permission(self):
        """
        ログインユーザー以上にモデルの変更権限がある
        """
        self._test('adam', 'change')
        self._test('seele', 'change')
        self._test('nerv', 'change')
        self._test('children', 'change')
        self._test('wille', 'change', neg=True)
        self._test('anonymous', 'change', neg=True)
        self._test('administrator', 'change')
        self._test('project_member', 'change')

    def test_change_permission_with_obj(self):
        """
        以下のユーザーがオブジェクトの変更権限を持つ
        - ネルフ以上のメンバー
        - Productの管理者
        - 関連プロジェクトのメンバー
        """
        self._test('adam', 'change', obj=self.product)
        self._test('seele', 'change', obj=self.product)
        self._test('nerv', 'change', obj=self.product)
        self._test('children', 'change', obj=self.product, neg=True)
        self._test('wille', 'change', obj=self.product, neg=True)
        self._test('anonymous', 'change', obj=self.product, neg=True)
        self._test('administrator', 'change', obj=self.product)
        self._test('project_member', 'change', obj=self.product)

    def test_delete_permission(self):
        """
        ログインユーザー以上にモデルの削除権限がある
        """
        self._test('adam', 'delete')
        self._test('seele', 'delete')
        self._test('nerv', 'delete')
        self._test('children', 'delete')
        self._test('wille', 'delete', neg=True)
        self._test('anonymous', 'delete', neg=True)
        self._test('administrator', 'delete')
        self._test('project_member', 'delete')

    def test_delete_permission_with_obj(self):
        """
        以下のユーザーがオブジェクトの削除権限を持つ
        - Productの管理者
        """
        self._test('adam', 'delete', obj=self.product)
        self._test('seele', 'delete', obj=self.product, neg=True)
        self._test('nerv', 'delete', obj=self.product, neg=True)
        self._test('children', 'delete', obj=self.product, neg=True)
        self._test('wille', 'delete', obj=self.product, neg=True)
        self._test('anonymous', 'delete', obj=self.product, neg=True)
        self._test('administrator', 'delete', obj=self.product)
        self._test('project_member', 'delete', obj=self.product, neg=True)

    def test_join_permission(self):
        """
        ログインユーザー以上にモデルの参加権限がある
        """
        self._test('adam', 'join')
        self._test('seele', 'join')
        self._test('nerv', 'join')
        self._test('children', 'join')
        self._test('wille', 'join', neg=True)
        self._test('anonymous', 'join', neg=True)
        self._test('administrator', 'join')
        self._test('project_member', 'join')

    def test_join_permission_with_obj(self):
        """
        ログインユーザー以上、かつ既に参加者じゃない人に参加する権限がある
        """
        self._test('adam', 'join', obj=self.product)
        self._test('seele', 'join', obj=self.product)
        self._test('nerv', 'join', obj=self.product)
        self._test('children', 'join', obj=self.product)
        self._test('wille', 'join', obj=self.product, neg=True)
        self._test('anonymous', 'join', obj=self.product, neg=True)
        self._test('administrator', 'join', obj=self.product, neg=True)
        self._test('project_member', 'join', obj=self.product)

    def test_quit_permission(self):
        """
        ログインユーザー以上にモデルの脱退権限がある
        """
        self._test('adam', 'quit')
        self._test('seele', 'quit')
        self._test('nerv', 'quit')
        self._test('children', 'quit')
        self._test('wille', 'quit', neg=True)
        self._test('anonymous', 'quit', neg=True)
        self._test('administrator', 'quit')
        self._test('project_member', 'quit')

    def test_quit_permission_with_obj(self):
        """
        最後ではない参加済みのユーザーのみがオブジェクトの脱退権限を持つ
        """
        self._test('adam', 'quit', obj=self.product)
        self._test('seele', 'quit', obj=self.product, neg=True)
        self._test('nerv', 'quit', obj=self.product, neg=True)
        self._test('children', 'quit', obj=self.product, neg=True)
        self._test('wille', 'quit', obj=self.product, neg=True)
        self._test('anonymous', 'quit', obj=self.product, neg=True)
        self._test('project_member', 'quit', obj=self.product, neg=True)

        # 最後の一人なので脱退できない
        self._test('administrator', 'quit', obj=self.product, neg=True)

        # もう一人参加者を増やす
        new_administrator = PersonaFactory()
        self.product.join(new_administrator)

        # django-permissionのキャッシュの問題で権限が更新されないので
        # オブジェクトを再度取得している
        self.users['administrator'] = Persona.objects.get(
            pk=self.users['administrator'].pk,
        )

        # 最後の一人になるので同じ人が脱退できるようになる
        self._test('administrator', 'quit', obj=self.product)
