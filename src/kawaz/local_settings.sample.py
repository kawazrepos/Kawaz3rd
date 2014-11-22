###############################################################################
#
#   本番用設定サンプル
#
###############################################################################
from .pre_settings import *

# Sessionの暗号化などに使用されるキーを変更。
# セキュリティリスクを避けるためにこの文字列は公開してはいけない
# Ref: https://docs.djangoproject.com/en/1.7/ref/settings/#secret-key
SECRET_KEY = 'ここに十分に長いランダムな文字列'

ALLOWED_HOSTS = (
    '127.0.0.1', 'localhost',
)

DEBUG = True
PRODUCT = False
TEMPLATE_DEBUG = DEBUG

# パターン青（深刻なエラー等）が発生した場合にメール通知を受けるための
# メールアドレスを記載
ADMINS = (
    ('管理者', 'webmaster@kawaz.org'),
)

# 高速化のためのキャッシュメカニズムを指定
# Ref: http://docs.djangoproject.jp/en/latest/topics/cache.html
if PRODUCT:
    CACHES = {
        'default': {
            # 本番環境では下記を利用
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

# 本番用データーベースの設定
if PRODUCT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mydatabase',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }

# メール用の設定を記載
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# プラグインの設定 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# django-permission
# パーミッションが存在するか否かのテストを行わない
PERMISSION_CHECK_PERMISSION_PRESENCE = False

# django-inspectional-registration
# 管理者用のメールアドレス
# 新規会員登録がされたとき、このメールアドレス宛てに通知が届きます
REGISTRATION_NOTIFICATION_RECIPIENTS = (
    'webmaster@kawaz.org',
)

# django-activities
if PRODUCT:
    ACTIVITIES_INSTALLED_NOTIFIERS = (
        ('twitter_kawaz_official',
         'activities.notifiers.oauth.twitter.TwitterActivityNotifier',
         os.path.join(CONFIG_ROOT, 'activities', 'notifiers',
                      'credentials_twitter_kawaz_official.json')),
        ('twitter_kawaz_info',
         'activities.notifiers.oauth.twitter.TwitterActivityNotifier',
         os.path.join(CONFIG_ROOT, 'activities', 'notifiers',
                      'credentials_twitter_kawazinfo.json')),
    )

# django-compress
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = PRODUCT

# django-google-calendar
if PRODUCT:
    GCAL_CALENDAR_ID = (
        # 本番用Google Calendar
    )

LOCAL_SETTINGS_LOADED = True
