from django.test import TestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.tests.testcases.permissions import BasePermissionLogicTestCase
from ..models import Star
from .factories import ArticleFactory, StarFactory


class StarPermissionLogicTestCase(BasePermissionLogicTestCase):
    app_label = 'stars'
    model_name = 'star'

    def setUp(self):
        super().setUp()

        self.article_author = PersonaFactory(username='article_author',
                                             role='children')
        self.star_author = PersonaFactory(username='star_author',
                                          role='children')
        self.users['article_author'] = self.article_author
        self.users['star_author'] = self.article_author
        self.article = ArticleFactory(author=self.article_author)
        self.protected_article = ArticleFactory(author=self.article_author,
                                                pub_state='protected')
        self.star = StarFactory(content_object=self.article,
                                author=self.star_author)
        self.protected_star = StarFactory(content_object=self.protected_article,
                                          author=self.star_author)

    def test_add_star_permission(self):
        """
        メンバーはスターを追加する権限を持つがそれ以外は持たない
        """
        self._test('adam', 'add')
        self._test('seele', 'add')
        self._test('nerv', 'add')
        self._test('children', 'add')
        self._test('wille', 'add', neg=True)
        self._test('anonymous', 'add', neg=True)

    def test_change_permission_without_obj(self):
        """
        基本的に変更権限は誰も持たない（神を除く）
        """
        self._test('adam', 'change')
        self._test('seele', 'change', neg=True)
        self._test('nerv', 'change', neg=True)
        self._test('children', 'change', neg=True)
        self._test('wille', 'change', neg=True)
        self._test('anonymous', 'change', neg=True)

    def test_change_permission_with_obj(self):
        """
        基本的に変更権限は誰も持たない（神を除く）
        """
        self._test('adam', 'change', obj=self.star)
        self._test('seele', 'change', obj=self.star, neg=True)
        self._test('nerv', 'change', obj=self.star, neg=True)
        self._test('children', 'change', obj=self.star, neg=True)
        self._test('wille', 'change', obj=self.star, neg=True)
        self._test('anonymous', 'change', obj=self.star, neg=True)
        # スターの所有者・スター先の所有者も持たない
        self._test('star_author', 'change', obj=self.star, neg=True)
        self._test('article_author', 'change', obj=self.star, neg=True)

    def test_delete_permission_without_obj(self):
        """
        メンバーはスターを消去する権限を持つが、それ以外は持たない
        """
        self._test('adam', 'delete')
        self._test('seele', 'delete')
        self._test('nerv', 'delete')
        self._test('children', 'delete')
        self._test('wille', 'delete', neg=True)
        self._test('anonymous', 'delete', neg=True)

    def test_delete_permission_with_obj(self):
        """
        スターもしくはスター先オブジェクトの所有者のみがスターを削除する権限
        を持つ
        """
        self._test('adam', 'delete', obj=self.star)
        self._test('seele', 'delete', obj=self.star, neg=True)
        self._test('nerv', 'delete', obj=self.star, neg=True)
        self._test('children', 'delete', obj=self.star, neg=True)
        self._test('wille', 'delete', obj=self.star, neg=True)
        self._test('anonymous', 'delete', obj=self.star, neg=True)
        # スターの所有者・スター先の所有者は持つ
        self._test('article_author', 'delete', obj=self.star)
        self._test('star_author', 'delete', obj=self.star)

    def test_view_permission_without_obj(self):
        """
        あらゆるユーザーがスターを見る権限を持つ可能性がある
        """
        self._test('adam', 'view')
        self._test('seele', 'view')
        self._test('nerv', 'view')
        self._test('children', 'view')
        self._test('wille', 'view')
        self._test('anonymous', 'view')

    def test_view_permission_with_obj(self):
        """
        あらゆるユーザーがスターを見る権限を持つ
        """
        self._test('adam', 'view', obj=self.star)
        self._test('seele', 'view', obj=self.star)
        self._test('nerv', 'view', obj=self.star)
        self._test('children', 'view', obj=self.star)
        self._test('wille', 'view', obj=self.star)
        self._test('anonymous', 'view', obj=self.star)

    def test_view_permission_with_protected_obj(self):
        """
        メンバーのみ内部公開に付加されたスターを閲覧できる
        """
        self._test('adam', 'view', obj=self.protected_star)
        self._test('seele', 'view', obj=self.protected_star)
        self._test('nerv', 'view', obj=self.protected_star)
        self._test('children', 'view', obj=self.protected_star)
        self._test('wille', 'view', obj=self.protected_star, neg=True)
        self._test('anonymous', 'view', obj=self.protected_star, neg=True)

