
from unittest.mock import patch
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.tests.testcases.permissions import BasePermissionLogicTestCase
from .factories import Comment, CommentTestArticle, CommentFactory
from ..perms import CommentPermissionLogic


class CommentPermissionLogicTestCase(BasePermissionLogicTestCase):
    app_label = 'django_comments'
    model_name = 'comment'

    def setUp(self):
        super().setUp()

        self.article_author = PersonaFactory(username='article_author',
                                             role='children')
        self.comment_author = PersonaFactory(username='comment_author',
                                             role='children')
        self.users['article_author'] = self.article_author
        self.users['comment_author'] = self.comment_author
        self.article = CommentTestArticle(author=self.article_author)
        self.article.save()
        self.comment = CommentFactory(content_object=self.article,
                                      user=self.comment_author)

    def test_add_comment_permission(self):
        """
        メンバーはコメントを追加する権限を持つがそれ以外は持たない
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
        self._test('adam', 'change', obj=self.comment)
        self._test('seele', 'change', obj=self.comment, neg=True)
        self._test('nerv', 'change', obj=self.comment, neg=True)
        self._test('children', 'change', obj=self.comment, neg=True)
        self._test('wille', 'change', obj=self.comment, neg=True)
        self._test('anonymous', 'change', obj=self.comment, neg=True)
        # コメントの所有者・コメント先の所有者も持たない
        self._test('comment_author', 'change', obj=self.comment, neg=True)
        self._test('article_author', 'change', obj=self.comment, neg=True)

    def test_delete_permission_without_obj(self):
        """
        基本的に削除権限は誰も持たない（神を除く）
        """
        self._test('adam', 'delete')
        self._test('seele', 'delete', neg=True)
        self._test('nerv', 'delete', neg=True)
        self._test('children', 'delete', neg=True)
        self._test('wille', 'delete', neg=True)
        self._test('anonymous', 'delete', neg=True)

    def test_delete_permission_with_obj(self):
        """
        基本的に削除権限は誰も持たない（神を除く）
        """
        self._test('adam', 'delete', obj=self.comment)
        self._test('seele', 'delete', obj=self.comment, neg=True)
        self._test('nerv', 'delete', obj=self.comment, neg=True)
        self._test('children', 'delete', obj=self.comment, neg=True)
        self._test('wille', 'delete', obj=self.comment, neg=True)
        self._test('anonymous', 'delete', obj=self.comment, neg=True)
        # コメントの所有者・コメント先の所有者も持たない
        self._test('article_author', 'delete', obj=self.comment, neg=True)
        self._test('comment_author', 'delete', obj=self.comment, neg=True)

    def test_delete_permission_with_target_obj(self):
        """
        オブジェクトの所有者（編集権限所有者）も所属コメントを削除する権限を持たない（神除く）
        """
        self._test('adam', 'delete', obj=self.article)
        self._test('seele', 'delete', obj=self.article, neg=True)
        self._test('nerv', 'delete', obj=self.article, neg=True)
        self._test('children', 'delete', obj=self.article, neg=True)
        self._test('wille', 'delete', obj=self.article, neg=True)
        self._test('anonymous', 'delete', obj=self.article, neg=True)
        # オブジェクトの編集権限所有者はコメントの削除権限も持たない
        self._test('article_author', 'delete', obj=self.comment, neg=True)
        self._test('comment_author', 'delete', obj=self.comment, neg=True)

    def test_can_moderate_permission(self):
        """
        ログインユーザーはコメントを非表示にする権限を持つ
        """
        self.use_model_name = False
        self._test('adam', 'can_moderate')
        self._test('seele', 'can_moderate')
        self._test('nerv', 'can_moderate')
        self._test('children', 'can_moderate')
        self._test('wille', 'can_moderate', neg=True)
        self._test('anonymous', 'can_moderate', neg=True)
        # コメントの所有者・コメント先の所有者も非表示にする権限を持つ
        self._test('article_author', 'can_moderate', obj=self.comment)
        self._test('comment_author', 'can_moderate', obj=self.comment)
        self.use_model_name = True

    def test_can_moderate_with_obj(self):
        """
        コメントを書いた人と、コメントが付いた記事作者と、ネルフ以上のみが非表示にする権限を持つ
        """
        self.use_model_name = False
        self._test('adam', 'can_moderate', obj=self.comment)
        self._test('seele', 'can_moderate', obj=self.comment)
        self._test('nerv', 'can_moderate', obj=self.comment)
        self._test('children', 'can_moderate', obj=self.comment, neg=True)
        self._test('wille', 'can_moderate', obj=self.comment, neg=True)
        self._test('anonymous', 'can_moderate', obj=self.comment, neg=True)
        # オブジェクトの編集権限所有者はコメントを非表示にする権限を持つ
        self._test('comment_author', 'can_moderate', obj=self.comment)
        self._test('comment_author', 'can_moderate', obj=self.comment)
        self.use_model_name = True
