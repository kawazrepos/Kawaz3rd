import os
import json
import tempfile
from django.conf import settings
from rest_framework.test import APITestCase

from .factories import MaterialFactory

from kawaz.core.personas.tests.factories import PersonaFactory


class MaterialAPITestCase(APITestCase):

    def _login_with_role(self, role):
        if not role == 'anonymous':
            user = PersonaFactory(role=role)
            self.client.force_authenticate(user=user)


class MaterialCreateAPITestCase(MaterialAPITestCase):

    def _test_create_material_with_user(self, role, success):
        path = os.path.join(settings.STATICFILES_DIRS[-1], 'fixtures', 'attachments', 'system', 'kawaztan.png')
        self.assertTrue(os.path.exists(path))
        with open(path, 'rb') as file:
            data = {
                'content_file' : file
            }
            r = self.client.post('/attachments/materials.json', data)
            if success:
                self.assertEqual(r.status_code, 201,
                                 '{} should upload materials via API'.format(role))
            else:
                self.assertEqual(r.status_code, 403,
                                 '{} should not be enable to upload material via API'.format(role))


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

class MaterialUpdateAPITestCase(MaterialAPITestCase):

    def setUp(self):
        self.material = MaterialFactory()

    def _update_with_role(self, role):
        self._login_with_role(role)
        path = os.path.join(settings.STATICFILES_DIRS[-1], 'fixtures', 'attachments', 'system', 'kawaztan.png')
        self.assertTrue(os.path.exists(path))

        with open(path, 'rb') as file:
            data = {
                'content_file' : file
            }
            r = self.client.put('/attachments/materials/{}.json'.format(self.material.slug), data)
            self.assertEqual(r.status_code, 404,
                             '{} should not update materials via API'.format(role))

    def test_update_material_via_api(self):
        """
        どのユーザーがupdateAPIを叩いても404が返ってくる
        """
        self._update_with_role('seele')
        self._update_with_role('nerv')
        self._update_with_role('children')
        self._update_with_role('wille')
        self._update_with_role('anonymous')

class MaterialDeleteAPITestCase(MaterialAPITestCase):

    def setUp(self):
        self.material = MaterialFactory()

    def _delete_with_role(self, role):
        self._login_with_role(role)

        r = self.client.delete('/attachments/materials/{}.json'.format(self.material.slug))
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

class MaterialRetrieveAPITestCase(MaterialAPITestCase):

    def setUp(self):
        self.material = MaterialFactory()

    def _retrieve_with_role(self, role):
        self._login_with_role(role)
        path = os.path.join(settings.STATICFILES_DIRS[-1], 'fixtures', 'attachments', 'system', 'kawaztan.png')
        self.assertTrue(os.path.exists(path))

        with open(path, 'rb') as file:
            r = self.client.get('/attachments/materials/{}.json'.format(self.material.slug))
            self.assertEqual(r.status_code, 404,
                             '{} should not retrieve materials via API'.format(role))

    def test_retrieve_material_via_api(self):
        """
        どのユーザーがretrieveのAPIを叩いても404が返ってくる
        """
        self._retrieve_with_role('seele')
        self._retrieve_with_role('nerv')
        self._retrieve_with_role('children')
        self._retrieve_with_role('wille')
        self._retrieve_with_role('anonymous')


class MaterialListAPITestCase(MaterialAPITestCase):

    def setUp(self):
        self.material = MaterialFactory()

    def _list_with_role(self, role):
        self._login_with_role(role)
        path = os.path.join(settings.STATICFILES_DIRS[-1], 'fixtures', 'attachments', 'system', 'kawaztan.png')
        self.assertTrue(os.path.exists(path))

        with open(path, 'rb') as file:
            r = self.client.get('/attachments/materials.json'.format(self.material.slug))
            self.assertEqual(r.status_code, 405,
                             '{} should not access to lists of materials via API'.format(role))

    def test_list_material_via_api(self):
        """
        どのユーザーがlistのAPIを叩いても405が返ってくる
        """
        self._list_with_role('seele')
        self._list_with_role('nerv')
        self._list_with_role('children')
        self._list_with_role('wille')
        self._list_with_role('anonymous')
