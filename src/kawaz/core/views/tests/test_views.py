from django.test import TestCase
from django.core.urlresolvers import reverse

from kawaz.core.personas.tests.factories import PersonaFactory

class KawazIndexViewTestCase(TestCase):

    def test_anonymous_user(self):
        """
        非ログインユーザーはAnonymousIndexにリダイレクトされます
        """
        response = self.client.get("")
        self.assertTemplateUsed(response, 'core/anonymous_index.html')

    def test_authorized_user(self):
        """
        ログインユーザーはAuthorizedIndexにリダイレクトされます
        """
        user = PersonaFactory()

        self.assertTrue(self.client.login(username=user.username, password='password'))
        response = self.client.get("")
        self.assertTemplateUsed(response, 'core/authenticated_index.html')


class KawazAnonymousIndexViewTestCase(TestCase):

    def test_unauthorized_context(self):
        """
        非ログインユーザーがトップにアクセスしたとき、以下のQuerySetがcontextに含まれます
        recent_products : display_mode = normalのプロダクトリリース日順3件
        featured_products : display_mode = featureのリリース日順全て
        products : display_mode = feature || tiled のリリース日順全て
        entries : publicなブログ記事公開日順5件
        events : publicでアクティブなイベント開催日時が近い順5件
        announcements : publicなお知らせ公開日順5件
        """
        r = self.client.get("/")
        self.assertIsNotNone(r.context['recent_products'])
        self.assertIsNotNone(r.context['featured_products'])
        self.assertIsNotNone(r.context['products'])
        self.assertIsNotNone(r.context['entries'])
        self.assertIsNotNone(r.context['events'])
        self.assertIsNotNone(r.context['announcements'])
