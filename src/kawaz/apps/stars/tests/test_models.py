from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.tests.utils import create_role_users
from ..models import Star
from .factories import StarFactory, ArticleFactory


class StarManagerTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='author', role='children')
        self.articles = dict(
            public=ArticleFactory(pub_state='public'),
            public2=ArticleFactory(pub_state='public'),
            public3=ArticleFactory(pub_state='public'),
            protected=ArticleFactory(pub_state='protected'),
            draft=ArticleFactory(pub_state='draft'),
        )

    def test_add_to_object(self):
        """スター追加テスト"""
        previous_count = Star.objects.count()
        for pub_state, article in self.articles.items():
            instance = Star.objects.add_to_object(article, self.user)
            self.assertIsNotNone(instance)
            self.assertTrue(Star.objects.count(), previous_count + 1)
            previous_count += 1

    def test_add_to_object_with_quote(self):
        """引用文字列付きのスターの付加テスト

        引用（quote）はJavaScriptなどで付加を行うのでAPI的にはあらゆる文字列
        が付加可能になっている。
        """
        previous_count = Star.objects.count()
        quote = "テスト"
        for pub_state, article in self.articles.items():
            instance = Star.objects.add_to_object(article, self.user,
                                                  quote=quote)
            self.assertIsNotNone(instance)
            self.assertEqual(instance.quote, quote)
            self.assertTrue(Star.objects.count(), previous_count + 1)
            previous_count += 1

    def test_remove_from_object(self):
        """スターの削除テスト"""
        article = self.articles['public']
        previous_count = Star.objects.count()
        # 強制的にスターを作成
        instance = StarFactory(author=self.user,
                               content_object=article)
        # 削除テスト
        Star.objects.remove_from_object(article, instance)
        self.assertEqual(Star.objects.count(), previous_count)

    def test_remove_from_object_with_wrong_object(self):
        """存在しないスターの削除テスト

        指定したスターが指定したオブジェクトに存在しない場合は
        ObjectDoesNotExist が発生する
        """
        article = self.articles['public']
        article2 = self.articles['public2']
        # 強制的にスターを作成
        instance = StarFactory(author=self.user,
                               content_object=article)
        # 削除テスト（aritcle2にはstarが付加されていない）
        self.assertRaises(ObjectDoesNotExist,
                          Star.objects.remove_from_object,
                          article2, instance)

    def test_get_for_object(self):
        """指定されたオブジェクトに関連付けられたスターを取得するテスト"""
        article1 = self.articles['public']
        article2 = self.articles['public2']
        article3 = self.articles['public3']

        for i in range(1):
            StarFactory(content_object=article1)
        for i in range(2):
            StarFactory(content_object=article2)
        for i in range(3):
            StarFactory(content_object=article3)

        self.assertEqual(Star.objects.get_for_object(article1).count(), 1)
        self.assertEqual(Star.objects.get_for_object(article2).count(), 2)
        self.assertEqual(Star.objects.get_for_object(article3).count(), 3)
        self.assertEqual(Star.objects.count(), 6)

    def test_cleanup_object(self):
        """指定されたオブジェクトからスターを全て取り除くテスト"""
        article1 = self.articles['public']
        article2 = self.articles['public2']
        article3 = self.articles['public3']

        for i in range(1):
            StarFactory(content_object=article1)
        for i in range(2):
            StarFactory(content_object=article2)
        for i in range(3):
            StarFactory(content_object=article3)

        Star.objects.cleanup_object(article1)
        Star.objects.cleanup_object(article2)
        Star.objects.cleanup_object(article3)

        self.assertEqual(Star.objects.get_for_object(article1).count(), 0)
        self.assertEqual(Star.objects.get_for_object(article2).count(), 0)
        self.assertEqual(Star.objects.get_for_object(article3).count(), 0)
        self.assertEqual(Star.objects.count(), 0)

    def test_published(self):
        """ユーザーが閲覧可能なスターの一覧を返す"""
        article1 = self.articles['public']
        article2 = self.articles['protected']
        article3 = self.articles['draft']
        users = create_role_users()

        for i in range(1):
            StarFactory(content_object=article1)
        for i in range(2):
            StarFactory(content_object=article2)
        for i in range(3):
            StarFactory(content_object=article3)

        patterns = (
            ('adam', 3),
            ('seele', 3),
            ('nerv', 3),
            ('children', 3),
            ('wille', 1),
            ('anonymous', 1),
        )
        for role, nstars in patterns:
            qs = Star.objects.published(users[role])
            self.assertEqual(qs.count(), nstars,
                             "{} should see {} stars".format(role, nstars))
