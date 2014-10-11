import os
import json
from django.conf import settings
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import MaterialFactory


LIST_URL_NAME = 'material-list'
TEST_FILENAME = os.path.join(os.path.dirname(__file__),
                             'data', 'kawaztan.png')


class MaterialAPITestCaseBase(APITestCase):
    def _login_with_role(self, role):
        if not role == 'anonymous':
            user = PersonaFactory(role=role)
            self.client.force_authenticate(user=user)


class MaterialCreateAPITestCase(MaterialAPITestCaseBase):
    def _test_create_material_with_user(self, role, success):
        self._login_with_role(role)
        path = TEST_FILENAME
        self.assertTrue(os.path.exists(path))
        with open(path, 'rb') as fi:
            data = {
                'content_file': fi
            }
            url = reverse(LIST_URL_NAME)
            r = self.client.post(url, data)
            if success:
                self.assertEqual(r.status_code, 201,
                                 '{} should upload materials '
                                 'via API'.format(role))
                dict = json.loads(r.content.decode())
                self.assertTrue('tag' in dict)
                self.assertTrue('slug' in dict)
                self.assertTrue('author' in dict)
                self.assertTrue('ip_address' in dict)
                self.assertTrue('content_file' in dict)
            else:
                self.assertEqual(r.status_code, 403,
                                 '{} should not be enable to '
                                 'upload material via API'.format(role))

    def test_create_material_via_api(self):
        """
        seele/nerv/childrenが/api/materials/から素材をアップロードできる
        """
        self._test_create_material_with_user('seele', True)
        self._test_create_material_with_user('nerv', True)
        self._test_create_material_with_user('children', True)

    def test_cannot_create_material_via_api(self):
        """
        wille/annonymousは/api/materials/から素材をアップロードできない
        """
        self._test_create_material_with_user('wille', False)
        self._test_create_material_with_user('anonymous', False)


class MaterialUpdateAPITestCase(MaterialAPITestCaseBase):
    def setUp(self):
        self.material = MaterialFactory()

    def _update_with_role(self, role):
        self._login_with_role(role)
        path = TEST_FILENAME
        self.assertTrue(os.path.exists(path))

        with open(path, 'rb') as fi:
            data = {
                'content_file': fi
            }
            # detail URL は存在してないので detail URL っぽい URL
            # を指定してみる
            url = reverse(LIST_URL_NAME)
            url = url + "/{}/".format(self.material.slug)
            r = self.client.put(url, data)
            self.assertEqual(r.status_code, 404,
                             '{} should not update materials '
                             'via API'.format(role))

    def test_update_material_via_api(self):
        """
        どのユーザーがupdateAPIを叩いても404が返ってくる
        """
        self._update_with_role('seele')
        self._update_with_role('nerv')
        self._update_with_role('children')
        self._update_with_role('wille')
        self._update_with_role('anonymous')


class MaterialDeleteAPITestCase(MaterialAPITestCaseBase):
    def setUp(self):
        self.material = MaterialFactory()

    def _delete_with_role(self, role):
        self._login_with_role(role)
        # detail URL は存在してないので detail URL っぽい URL
        # を指定してみる
        url = reverse(LIST_URL_NAME)
        url = url + "/{}/".format(self.material.slug)
        r = self.client.delete(url)
        self.assertEqual(r.status_code, 404,
                         '{} should not delete materials via API'.format(role))

    def test_delete_material_via_api(self):
        """
        どのユーザーがdeleteのAPIを叩いても404が返ってくる
        """
        self._delete_with_role('seele')
        self._delete_with_role('nerv')
        self._delete_with_role('children')
        self._delete_with_role('wille')
        self._delete_with_role('anonymous')


class MaterialRetrieveAPITestCase(MaterialAPITestCaseBase):
    def setUp(self):
        self.material = MaterialFactory()

    def _retrieve_with_role(self, role):
        self._login_with_role(role)
        path = TEST_FILENAME
        self.assertTrue(os.path.exists(path))

        # detail URL は存在してないので detail URL っぽい URL
        # を指定してみる
        url = reverse(LIST_URL_NAME)
        url = url + "/{}/".format(self.material.slug)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404,
                         '{} should not retrieve materials '
                         'via API'.format(role))

    def test_retrieve_material_via_api(self):
        """
        どのユーザーがretrieveのAPIを叩いても404が返ってくる
        """
        self._retrieve_with_role('seele')
        self._retrieve_with_role('nerv')
        self._retrieve_with_role('children')
        self._retrieve_with_role('wille')
        self._retrieve_with_role('anonymous')


class MaterialListAPITestCase(MaterialAPITestCaseBase):
    def setUp(self):
        self.material = MaterialFactory()

    def _list_with_role(self, role):
        self._login_with_role(role)
        path = TEST_FILENAME
        self.assertTrue(os.path.exists(path))

        url = reverse(LIST_URL_NAME)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 405,
                         '{} should not access to lists of '
                         'materials via API'.format(role))

    def test_list_material_via_api(self):
        """
        どのユーザーがlistのAPIを叩いても405が返ってくる
        """
        self._list_with_role('seele')
        self._list_with_role('nerv')
        self._list_with_role('children')
        self._list_with_role('wille')
        self._list_with_role('anonymous')
