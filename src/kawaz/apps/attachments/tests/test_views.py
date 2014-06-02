import os
import shutil
import tempfile
from django.conf import settings
from django.test import TestCase
from .factories import MaterialFactory
from ..models import Material

class MaterialDetailViewTestCase(TestCase):
    media_root = ''

    def setUp(self):
        # ユーザーとユーザー用のディレクトリを作成
        self.media_root = tempfile.mkdtemp()
        self.original_setting = settings.MEDIA_ROOT
        # override_settingsは、遅延して設定できないようなので
        # 普通にsettingsを変更している
        settings.MEDIA_ROOT = self.media_root

    def _generate_material(self, ext=None):
        """
        拡張子がextの一時ファイルを生成します
        @return Material
        """
        path = os.path.join(self.media_root, 'attachments', 'username')
        if not os.path.exists(path): os.makedirs(path)
        tmp_file = tempfile.mkstemp(dir=path, suffix=ext)[1]
        print(tmp_file)
        name = os.path.split(tmp_file)[-1]
        settings.MEDIA_ROOT = self.media_root
        material = MaterialFactory(content_file=name, author__username='username')
        self.assertTrue(os.path.exists(material.content_file.path))
        return material

    def tearDown(self):
        # tmpfileを削除
        shutil.rmtree(self.media_root)
        settings.MEDIA_ROOT = self.original_setting

    def _download_file(self, ext):
        """
        拡張子がextのファイルをダウンロードします
        @return HttpResponse
        @return Material
        """
        material = self._generate_material(ext)
        r = self.client.get(material.get_absolute_url())
        return r, material

    def _test_mimetype(self, ext, mimetype):
        """
        extのmimetypeが正しいかをチェックします
        """
        r, material = self._download_file(ext)
        content_type = r['content-type']
        self.assertEqual(content_type, mimetype)

    def test_not_found(self):
        """
        ファイルが存在しないMaterialを読もうとしたとき、404を送出するか
        また、このときレコードは削除される
        """
        material = MaterialFactory()

        self.assertEqual(Material.objects.count(), 1)
        r = self.client.get(material.get_absolute_url())
        self.assertEqual(r.status_code, 404)
        self.assertEqual(Material.objects.count(), 0)

    def test_check_mimetype(self):
        """
        viewが正しいmimetypeを返すか
        """
        self._test_mimetype('.png', 'image/png')
        self._test_mimetype('.jpg', 'image/jpeg')
        self._test_mimetype('.mp3', 'audio/mpeg')

    def test_check_content_disposition(self):
        """
        viewが正しいContent-Dispositionを返すか
        """
        r, material = self._download_file('.zip')
        self.assertEqual(r['Content-Disposition'], 'attachment; filename={}'.format(material.filename))
