import datetime
from kawaz.core.tests.testcases.permissions import BasePermissionLogicTestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Entry, Category
from .factories import EntryFactory, CategoryFactory


class EntryPermissionLogicTestCase(BasePermissionLogicTestCase):
    app_label = 'blogs'
    model_name = 'entry'

    def setUp(self):
        super().setUp()
        self.users['author'] = PersonaFactory(username='author',
                                                 role='children')
        self.users['other'] = PersonaFactory(username='other',
                                                role='children')
        self.entry = EntryFactory(author=self.users['author'])

    def test_add_permission(self):
        """
        Children以上のユーザーがブログエントリーを作成できる
        """
        self._test('adam', 'add')
        self._test('seele', 'add')
        self._test('nerv', 'add')
        self._test('children', 'add')
        self._test('wille', 'add', neg=True)
        self._test('anonymous', 'add', neg=True)

    def test_change_permission_without_obj(self):
        """
        Children以上のユーザーはどれかのエントリーを変更できる
        """
        self._test('adam', 'change')
        self._test('seele', 'change')
        self._test('nerv', 'change')
        self._test('children', 'change')
        self._test('wille', 'change', neg=True)
        self._test('anonymous', 'change', neg=True)

    def test_change_permission_with_obj(self):
        """
        Children以上のユーザーは自分の書いたエントリーのみを変更できる
        ただしAdamは他人のでも変更できる
        """
        self._test('adam', 'change', obj=self.entry)
        self._test('seele', 'change', obj=self.entry, neg=True)
        self._test('nerv', 'change', obj=self.entry, neg=True)
        self._test('children', 'change', obj=self.entry, neg=True)
        self._test('wille', 'change', obj=self.entry, neg=True)
        self._test('anonymous', 'change', obj=self.entry, neg=True)
        self._test('author', 'change', obj=self.entry)

    def test_delete_permission_without_obj(self):
        """
        Children以上のユーザーはどれかのエントリーを削除できる
        """
        self._test('adam', 'delete')
        self._test('seele', 'delete')
        self._test('nerv', 'delete')
        self._test('children', 'delete')
        self._test('wille', 'delete', neg=True)
        self._test('anonymous', 'delete', neg=True)

    def test_delete_permission_with_obj(self):
        """
        Children以上のユーザーは自分の書いたエントリーのみを削除できる
        ただしAdamは他人のでも削除できる
        """
        self._test('adam', 'delete', obj=self.entry)
        self._test('seele', 'delete', obj=self.entry, neg=True)
        self._test('nerv', 'delete', obj=self.entry, neg=True)
        self._test('children', 'delete', obj=self.entry, neg=True)
        self._test('wille', 'delete', obj=self.entry, neg=True)
        self._test('anonymous', 'delete', obj=self.entry, neg=True)
        self._test('author', 'delete', obj=self.entry)


class EntryCategoryPermissionLogicTestCase(BasePermissionLogicTestCase):
    app_label = 'blogs'
    model_name = 'category'

    def setUp(self):
        super().setUp()
        self.users['author'] = PersonaFactory(username='author',
                                                 role='children')
        self.users['other'] = PersonaFactory(username='other',
                                                role='children')
        self.entry = EntryFactory(author=self.users['author'])

    def test_add_permission(self):
        """
        Children以上のユーザーがブログカテゴリーを作成できる
        """
        self._test('adam', 'add')
        self._test('seele', 'add')
        self._test('nerv', 'add')
        self._test('children', 'add')
        self._test('wille', 'add', neg=True)
        self._test('anonymous', 'add', neg=True)

    def test_change_permission_without_obj(self):
        """
        Children以上のユーザーはどれかのカテゴリーを変更できる
        """
        self._test('adam', 'change')
        self._test('seele', 'change')
        self._test('nerv', 'change')
        self._test('children', 'change')
        self._test('wille', 'change', neg=True)
        self._test('anonymous', 'change', neg=True)

    def test_change_permission_with_obj(self):
        """
        Children以上のユーザーは自分の作ったカテゴリーのみを変更できる
        ただしAdamは他人のでも変更できる
        """
        self._test('adam', 'change', obj=self.entry)
        self._test('seele', 'change', obj=self.entry, neg=True)
        self._test('nerv', 'change', obj=self.entry, neg=True)
        self._test('children', 'change', obj=self.entry, neg=True)
        self._test('wille', 'change', obj=self.entry, neg=True)
        self._test('anonymous', 'change', obj=self.entry, neg=True)
        self._test('author', 'change', obj=self.entry)

    def test_delete_permission_without_obj(self):
        """
        Children以上のユーザーはどれかのカテゴリーを削除できる
        """
        self._test('adam', 'delete')
        self._test('seele', 'delete')
        self._test('nerv', 'delete')
        self._test('children', 'delete')
        self._test('wille', 'delete', neg=True)
        self._test('anonymous', 'delete', neg=True)

    def test_delete_permission_with_obj(self):
        """
        Children以上のユーザーは自分の作ったカテゴリーのみを削除できる
        ただしAdamは他人のでも削除できる
        """
        self._test('adam', 'delete', obj=self.entry)
        self._test('seele', 'delete', obj=self.entry, neg=True)
        self._test('nerv', 'delete', obj=self.entry, neg=True)
        self._test('children', 'delete', obj=self.entry, neg=True)
        self._test('wille', 'delete', obj=self.entry, neg=True)
        self._test('anonymous', 'delete', obj=self.entry, neg=True)
        self._test('author', 'delete', obj=self.entry)

