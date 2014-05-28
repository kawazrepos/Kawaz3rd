from django.test import TestCase
from .factories import MaterialFactory

class MaterialModelTestCase(TestCase):

    def test_set_slug_automatically(self):
        """
        slugの値が自動的にcontent_file.nameから決まる
        attachments/<username>/<filename>をutf-8でエンコードし、sha1を取った値と等しい
        """
        material = MaterialFactory(author__username='material_kawaztan')
        expected = "2acf1e273e96b94ba26f76faf7a9b2b46199c0b1"
        self.assertEqual(material.slug, expected)

    def test_str_returns_correctly(self):
        """
        str(material)がファイル名を返す
        """
        material = MaterialFactory(content_file='fantastic_music.mp3')
        self.assertEqual(str(material), 'fantastic_music.mp3')

    def test_get_absolute_url(self):
        """
        material.get_absolute_url()が`attachments/<slug>/`を返します
        """
        material = MaterialFactory(author__username='material_kawaztan')
        self.assertEqual(material.get_absolute_url(), "/attachments/2acf1e273e96b94ba26f76faf7a9b2b46199c0b1/")

    def test_filename(self):
        """
        material.filenameがファイル名を返す
        """
        material = MaterialFactory(content_file='fantastic_music.mp3')
        self.assertEqual(material.filename, 'fantastic_music.mp3')

    def test_ext(self):
        """
        material.extが拡張子を返す
        """
        material = MaterialFactory(content_file='fantastic_music.mp3')
        self.assertEqual(material.ext, 'mp3')

    def test_ext_with_upper(self):
        """
        material.extが拡張子が大文字の時、小文字にして返す
        """
        material = MaterialFactory(content_file='fantastic_music.MP3')
        self.assertEqual(material.ext, 'mp3')

    def test_ext_with_multiple(self):
        """
        material.extが拡張子が複数あるとき、最後のみ返す
        """
        material = MaterialFactory(content_file='great_library.tar.gz')
        self.assertEqual(material.ext, 'gz')

    def test_ext_nothing(self):
        """
        material.extが拡張子がないとき、空白文字を返す
        """
        material = MaterialFactory(content_file='README')
        self.assertEqual(material.ext, '')

class MaterialModelFileTypeTestCase(TestCase):

    def _test_with_table(self, table, property_name):
        for ext, result in table.items():
            filename = 'filename.{}'.format(ext)
            material = MaterialFactory(content_file=filename)
            value = getattr(material, property_name)
            if result:
                self.assertTrue(value)
            else:
                self.assertFalse(value)

    def test_is_image(self):
        """
        material.is_imageが画像だった場合Trueを返す
        """
        table = {
            'png' : True,
            'jpg' : True,
            'jpeg' : True,
            'gif' : True,
            'mp3' : False,
            'wav' : False,
            'ogg' : False,
            'mov' : False,
            'mp4' : False,
            'pdf' : False,
            'zip' : False,
            'rar' : False
        }
        self._test_with_table(table, 'is_image')

    def test_is_audio(self):
        """
        ファイルが音声だった場合、material.is_audioがTrueを返す
        """
        table = {
            'png' : False,
            'jpg' : False,
            'jpeg' : False,
            'gif' : False,
            'mp3' : True,
            'wav' : True,
            'ogg' : True,
            'mov' : False,
            'mp4' : False,
            'pdf' : False,
            'zip' : False,
            'rar' : False
        }
        self._test_with_table(table, 'is_audio')


    def test_is_movie(self):
        """
        ファイルが動画だった場合、material.is_movieがTrueを返す
        """
        table = {
            'png' : False,
            'jpg' : False,
            'jpeg' : False,
            'gif' : False,
            'mp3' : False,
            'wav' : False,
            'ogg' : False,
            'mov' : True,
            'mp4' : True,
            'pdf' : False,
            'zip' : False,
            'rar' : False
        }
        self._test_with_table(table, 'is_movie')


    def test_is_pdf(self):
        """
        ファイルがPDFだった場合、material.is_pdfがTrueを返す
        """
        table = {
            'png' : False,
            'jpg' : False,
            'jpeg' : False,
            'gif' : False,
            'mp3' : False,
            'wav' : False,
            'ogg' : False,
            'mov' : False,
            'mp4' : False,
            'pdf' : True,
            'zip' : False,
            'rar' : False
        }
        self._test_with_table(table, 'is_pdf')

