# ! -*- coding: utf-8 -*-
#
#
#

import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Category

LIST_URL_NAME = 'category-list'

def response_to_dict(response):
    json_string = response.content.decode(encoding='UTF-8')
    return json.loads(json_string)


class BaseTestCase(TestCase):
    def setUp(self):
        persona_factory = lambda x: PersonaFactory(username=x, role=x)

        self.users = dict(
            adam=persona_factory('adam'),
            seele=persona_factory('seele'),
            nerv=persona_factory('nerv'),
            children=persona_factory('children'),
            wille=persona_factory('wille'),
            anonymous=AnonymousUser(),
        )

class CategoryCreateAPITestCase(BaseTestCase):
    def _test_create(self, user, neg=False):
        get_object_count = lambda: Category.objects.count()
        previous_object_count = get_object_count()
        if isinstance(user, str):
            user = self.users[user]
        if user is not None and not isinstance(user, AnonymousUser):
            self.assertTrue(self.client.login(
                username=user,
                password='password'))
        data = json.dumps({'label': 'Category'})
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
            category = Category.objects.get(pk=response_obj['id'])
            # check if the user correctly applied
            self.assertEqual(category.author, user)

    def test_api_create_adam(self):
        """カテゴリー作成テスト（adam）"""
        self._test_create('adam')

    def test_api_create_seele(self):
        """カテゴリー作成テスト（seele）"""
        self._test_create('seele')

    def test_api_create_nerv(self):
        """カテゴリー作成テスト（nerv）"""
        self._test_create('nerv')

    def test_api_create_children(self):
        """カテゴリー作成テスト（children）"""
        self._test_create('children')

    def test_api_create_wille(self):
        """カテゴリー作成テスト（wille）"""
        self._test_create('wille', neg=True)

    def test_api_create_anonymous(self):
        """カテゴリー作成テスト（anonymous）"""
        self._test_create('anonymous', neg=True)
