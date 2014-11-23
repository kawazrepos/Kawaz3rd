import shutil
import tempfile

from django.conf import settings


class TempMediaMixin(object):
    """
    Mixin to create MEDIA_ROOT in temp and tear down when complete.
    cf. http://www.caktusgroup.com/blog/2013/06/26/media-root-and-django-tests/
    """

    def setup_test_environment(self):
        "Create temp directory and update MEDIA_ROOT and default storage."
        super(TempMediaMixin, self).setup_test_environment()
        settings._original_media_root = settings.MEDIA_ROOT
        settings._original_file_storage = settings.DEFAULT_FILE_STORAGE
        self._temp_media = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self._temp_media
        settings.DEFAULT_FILE_STORAGE = (
            'django.core.files.storage.FileSystemStorage')

    def teardown_test_environment(self):
        "Delete temp storage."
        super(TempMediaMixin, self).teardown_test_environment()
        shutil.rmtree(self._temp_media, ignore_errors=True)
        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root
        settings.DEFAULT_FILE_STORAGE = settings._original_file_storage
        del settings._original_file_storage

# Requires Django 1.6+
from django.test.runner import DiscoverRunner


class MediaRootTestSuiteRunner(TempMediaMixin, DiscoverRunner):
    "Local test suite runner."


class KawazDiscoverRunner(MediaRootTestSuiteRunner):
    def setup_test_environment(self):
        super().setup_test_environment()
        settings.TESTING = True
        #
        # django-compress の COMPRESS_ENABLED の部分に下記のような記載がある
        #
        # > When COMPRESS_ENABLED is False the input will be rendered without
        # > any compression except for code with a mimetype matching one listed
        # > in the COMPRESS_PRECOMPILERS setting. These matching files are
        # > still passed to the precompiler before rendering.
        # ( http://django-compressor.readthedocs.org/
        #   en/latest/settings/#django.conf.settings.COMPRESS_ENABLED )
        #
        # この様に django-compress は DEBUG=True（COMPRESS_ENABLED=False）の
        # 場合でも coffee/less のコンパイルを行おうとする。それに伴いファイル
        # の更新チェックなど余計なコードが大量に走るためユニットテストが尋常
        # じゃないほど時間がかかることになる。
        # ユニットテストにおいて coffee/less がコンパイルされている必要性は
        # 皆無なので、この機能自体を停止することでテストの高速化を行なっている
        #
        settings.COMPRESS_ENABLED = False
        settings.COMPRESS_OFFLINE = False
        settings.COMPRESS_PRECOMPILERS = ()
        #
        # django-activities の通知機能がテスト中に走るととても遅い and API制限
        # に引っかかる可能性が高いためOAuthのポスト部分を無効化する
        #
        settings.ACTIVITIES_ENABLE_OAUTH_NOTIFICATION = False
