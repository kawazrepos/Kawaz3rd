from django.test import TestCase
from django.db.models import Q
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.personas.tests.utils import create_role_users
from .models import PublishmentTestArticle as Article
from ..lookups import published_lookup
from ..lookups import draft_lookup


class PublishmentLookupsTestCase(TestCase):
    def setUp(self):
        self.author = PersonaFactory(username='author', role='children')
        self.users = create_role_users({'author': self.author})
        self.articles = dict(
            public=Article.objects.create(title="public",
                                          author=self.users['author'],
                                          pub_state='public'),
            protected=Article.objects.create(title="protected",
                                             author=self.users['author'],
                                             pub_state='protected'),
            draft=Article.objects.create(title="draft",
                                         author=self.users['author'],
                                         pub_state='draft'),
        )

    def test_published_lookup(self):
        """
        ユーザーに対して公開されているオブジェクトを正しく返すかテスト

        メンバーである adam, seele, nerv, children, author は public/protected
        の二種類を取得し、それ以外は public のみを取得可能
        """
        patterns = (
            ('adam', 2),
            ('seele', 2),
            ('nerv', 2),
            ('children', 2),
            ('wille', 1),
            ('anonymous', 1),
            ('author', 2),
        )
        for role, narticles in patterns:
            q = published_lookup(self.users[role])
            self.assertTrue(isinstance(q, Q))
            qs = Article.objects.filter(q)
            self.assertEqual(qs.count(), narticles,
                             "{} should see {} published articles".format(
                                 role, narticles))

    def test_draft_lookup(self):
        """
        ユーザーが編集可能な下書きオブジェクトを正しく返すかテスト

        下書きオブジェクトの所有者である author とあらゆる権限を持つ adam のみ
        下書きオブジェクトを取得でき、それ以外は取得できない
        """
        patterns = (
            ('adam', 1),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
            ('author', 1),
        )
        for role, narticles in patterns:
            q = draft_lookup(self.users[role])
            self.assertTrue(isinstance(q, Q))
            qs = Article.objects.filter(q)
            self.assertEqual(qs.count(), narticles,
                             "{} should see {} draft articles".format(
                                 role, narticles))
