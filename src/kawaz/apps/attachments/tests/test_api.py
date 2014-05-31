import os
import json
import tempfile
from django.conf import settings
from rest_framework.test import APITestCase

from kawaz.core.personas.tests.factories import PersonaFactory

class MaterialCreateAPITestCase(APITestCase):
    def setUp(self):
        self.file = tempfile.NamedTemporaryFile(mode='rb')

    def tearDown(self):
        self.file.close()

    def _test_create_material_with_user(self, role, success):
        if not role == 'anonymous':
            user = PersonaFactory(role=role)
            self.client.force_authenticate(user=user)
        path = os.path.join(settings.MEDIA_ROOT, 'fixtures', 'attachments', 'system', 'kawaztan.png')
        self.assertTrue(os.path.exists(path))
        file = open(path, 'rb')
        data = {
            'content_file' : file
        }
        r = self.client.post('/attachments/materials.json', data)
        if success:
            self.assertEqual(r.status_code, 201, '{} should upload materials via API'.format(role))
        else:
            self.assertEqual(r.status_code, 403, '{} should not be enable to upload material via API'.format(role))

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