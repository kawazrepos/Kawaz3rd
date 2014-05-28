import os
import json
import tempfile
from django.test import TestCase
from django.conf import settings
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Material

class MaterialCreateAPITestCase(TestCase):
    def setUp(self):
        self.file = tempfile.NamedTemporaryFile(mode='rb')

    def tearDown(self):
        self.file.close()

    def _test_create_material_with_user(self, role, success):
        if not role == 'anonymous':
            user = PersonaFactory(role=role)
            self.assertTrue(self.client.login(username=user.username, password='password'))
        path = os.path.join(settings.MEDIA_ROOT, 'fixtures', 'attachments', 'system', 'kawaztan.png')
        data = json.dumps({
            'content_file' : {
                'Content-Type' : "image/png",
                "file" : "hogehogehoge",
                "name" : "test.png"
            }
        })
        r = self.client.post('/api/v1/attachments/material/', data, content_type='application/json')
        if success:
            self.assertEqual(r.status_code, 201, '{} should upload materials via API'.format(role))
        else:
            self.assertEqual(r.status_code, 401, '{} should not be enable to upload material via API'.format(role))

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
