import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Star
from .factories import ArticleFactory, StarFactory

LIST_URL_NAME = 'star-list'
DETAIL_URL_NAME = 'star-detail'


def response_to_dict(response):
    json_string = response.content.decode(encoding='UTF-8')
    return json.loads(json_string)


class BaseTestCase(TestCase):
    def setUp(self):
        persona_factory = lambda x: PersonaFactory(username=x, role=x)
        article_factory = lambda **kwargs: ArticleFactory(
            author=self.users['article_author'], **kwargs)
        star_factory = lambda **kwargs: StarFactory(
            author=self.users['star_author'], **kwargs)

        self.users = dict(
            adam=persona_factory('adam'),
            seele=persona_factory('seele'),
            nerv=persona_factory('nerv'),
            children=persona_factory('children'),
            wille=persona_factory('wille'),
            anonymous=AnonymousUser(),
            article_author=PersonaFactory(username='article_author',
                                          role='children'),
            star_author=PersonaFactory(username='star_author',
                                       role='children'),
        )
        self.article = article_factory()
        self.protected_article = article_factory(pub_state='protected')

        self.star0 = star_factory(content_object=self.article)
        self.star1 = star_factory(content_object=self.article)
        self.star2 = star_factory(content_object=self.protected_article)
        self.star3 = star_factory(content_object=self.protected_article)


class StarListAPITestCase(BaseTestCase):
    def _test_list(self, user, object_count, obj=None):
        if isinstance(user, str):
            user = self.users[user]
        if user is not None and not isinstance(user, AnonymousUser):
            self.assertTrue(self.client.login(
                username=user,
                password='password'))
        url = reverse(LIST_URL_NAME)
        if obj:
            ct = ContentType.objects.get_for_model(obj)
            url = url + "?content_type={}&object_id={:d}"
            url = url.format(ct.pk, obj.pk)
        response = self.client.get(url)
        response_obj = response_to_dict(response)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_obj)
        self.assertEqual(len(response_obj), object_count)

        if object_count > 0:
            star0 = response_obj[0]
            self.assertIsNotNone(star0['author']['nickname'])
            self.assertIsNotNone(star0['author']['gender'])
            self.assertIsNotNone(star0['author']['small_avatar'])
            self.assertIsNotNone(star0['author']['middle_avatar'])
            self.assertIsNotNone(star0['author']['large_avatar'])
            self.assertIsNotNone(star0['author']['huge_avatar'])
            self.assertIsNotNone(star0['author']['role'])
            self.assertIsNotNone(star0['author']['nickname'])

    def test_api_list(self):
        """スターリスト取得テスト"""
        self._test_list('adam', 4)
        self._test_list('seele', 4)
        self._test_list('nerv', 4)
        self._test_list('children', 4)
        self._test_list('wille', 2)
        self._test_list('anonymous', 2)

    def test_api_list_with_obj(self):
        """オブジェクト関連スターリスト取得テスト"""
        self._test_list('adam', 2, obj=self.article)
        self._test_list('seele', 2, obj=self.article)
        self._test_list('nerv', 2, obj=self.article)
        self._test_list('children', 2, obj=self.article)
        self._test_list('wille', 2, obj=self.article)
        self._test_list('anonymous', 2, obj=self.article)

    def test_api_list_with_protected_obj(self):
        """内部公開オブジェクト関連スターリスト取得テスト"""
        self._test_list('adam', 2, obj=self.protected_article)
        self._test_list('seele', 2, obj=self.protected_article)
        self._test_list('nerv', 2, obj=self.protected_article)
        self._test_list('children', 2, obj=self.protected_article)
        self._test_list('wille', 0, obj=self.protected_article)
        self._test_list('anonymous', 0, obj=self.protected_article)


class StarCreateAPITestCase(BaseTestCase):
    def _test_create(self, user, obj, neg=False):
        get_object_count = lambda: Star.objects.count()
        previous_object_count = get_object_count()
        if isinstance(user, str):
            user = self.users[user]
        if user is not None and not isinstance(user, AnonymousUser):
            self.assertTrue(self.client.login(
                username=user,
                password='password'))
        ct = ContentType.objects.get_for_model(obj)
        data = json.dumps({'content_type': ct.pk, 'object_id': obj.pk})
        url = reverse(LIST_URL_NAME)
        response = self.client.post(url, data=data,
                                    content_type='application/json')
        if neg:
            self.assertEqual(response.status_code, 403)
            self.assertEqual(get_object_count(), previous_object_count)
        else:
            self.assertEqual(response.status_code, 201)
            self.assertEqual(get_object_count(), previous_object_count + 1)
            # get instance from response_obj
            response_obj = response_to_dict(response)
            star = Star.objects.get(pk=response_obj['id'])
            # check if the user correctly applied
            self.assertEqual(star.author, user)

    def test_api_create_adam(self):
        """スター作成テスト（adam）"""
        self._test_create('adam', obj=self.article)

    def test_api_create_seele(self):
        """スター作成テスト（seele）"""
        self._test_create('seele', obj=self.article)

    def test_api_create_nerv(self):
        """スター作成テスト（nerv）"""
        self._test_create('nerv', obj=self.article)

    def test_api_create_children(self):
        """スター作成テスト（children）"""
        self._test_create('children', obj=self.article)

    def test_api_create_wille(self):
        """スター作成テスト（wille）"""
        self._test_create('wille', obj=self.article, neg=True)

    def test_api_create_anonymous(self):
        """スター作成テスト（anonymous）"""
        self._test_create('anonymous', obj=self.article, neg=True)


class StarDeleteAPITestCase(BaseTestCase):
    def _test_delete(self, user, obj, neg=False):
        get_object_count = lambda: Star.objects.count()
        previous_object_count = get_object_count()
        if isinstance(user, str):
            user = self.users[user]
        if user is not None and not isinstance(user, AnonymousUser):
            self.assertTrue(self.client.login(
                username=user,
                password='password'))
        url = reverse(DETAIL_URL_NAME, kwargs=dict(pk=obj.pk))
        response = self.client.delete(url, content_type='application/json')
        if neg:
            self.assertEqual(response.status_code, 403)
            self.assertEqual(get_object_count(), previous_object_count)
        else:
            self.assertEqual(response.status_code, 204)
            self.assertEqual(get_object_count(), previous_object_count - 1)

    def test_api_delete_adam(self):
        """スター削除テスト（adam）"""
        self._test_delete('adam', obj=self.star0)

    def test_api_delete_seele(self):
        """スター削除テスト（seele）"""
        self._test_delete('seele', obj=self.star0, neg=True)

    def test_api_delete_nerv(self):
        """スター削除テスト（nerv）"""
        self._test_delete('nerv', obj=self.star0, neg=True)

    def test_api_delete_children(self):
        """スター削除テスト（children）"""
        self._test_delete('children', obj=self.star0, neg=True)

    def test_api_delete_wille(self):
        """スター削除テスト（wille）"""
        self._test_delete('wille', obj=self.star0, neg=True)

    def test_api_delete_anonymous(self):
        """スター削除テスト（anonymous）"""
        self._test_delete('anonymous', obj=self.star0, neg=True)

    def test_api_delete_article_author(self):
        """スター削除テスト（article_author）"""
        self._test_delete('article_author', obj=self.star0)

    def test_api_delete_star_author(self):
        """スター削除テスト（star_author）"""
        self._test_delete('star_author', obj=self.star0)
