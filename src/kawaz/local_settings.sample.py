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
    '127.0.0.1', 'localhost', '.kawaz.org',
)

# サイト設定
SITE_ID = 1

# 起動モード指定
DEBUG = False
PRODUCT = False
TEMPLATE_DEBUG = DEBUG

# パターン青（深刻なエラー等）が発生した場合にメール通知を受けるための
# メールアドレスを記載
ADMINS = (
    ('管理者', 'webmaster@kawaz.org'),
    ('lambdalisue', 'lambdalisue+kawaz@hashnote.net'),
    ('giginet', 'giginet.net+kawaz@gmail.com'),
    ('miio', 'info@miio.info')
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
            'NAME': 'kawaz',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '',
            'OPTIONS': {
                'connect_timeout': 60,
            },
        }
    }

# ログ関係の設定
if PRODUCT:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'mail_admins': {
                'level': 'WARNING',
                'class': 'django.utils.log.AdminEmailHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'kawaz': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'kawaz': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

# メール用の設定を記載
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'webmaster@kawaz.org'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_EMAIL = 'webmaster@kawaz.org'
DEFAULT_FROM_EMAIL = DEFAULT_EMAIL

# プラグインの設定 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# django-permission
# パーミッションが存在するか否かのテストを行わない
PERMISSION_CHECK_PERMISSION_PRESENCE = False

# django-inspectional-registration
# 管理者用のメールアドレス
# 新規会員登録がされたとき、このメールアドレス宛てに通知が届きます
REGISTRATION_NOTIFICATION_RECIPIENTS = (
    ('管理者', 'webmaster@kawaz.org'),
    ('giginet', 'giginet.net+kawaz@gmail.com'),
    ('AttaQ', 'attaqjp@gmail.com')
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
        ('hipchat_kawaz_all',
         'kawaz.core.activities.notifiers.hipchat.HipChatActivityNotifier',
         'mytoken',
         'roomid',
         {'from_name': 'Kawazポータル', 'color': 'green', 'is_notify': True}
        )
)
ACTIVITIES_DEFAULT_NOTIFIERS = (
    'twitter_kawaz_info',
    'hipchat_kawaz_all',
)

# utils
if PRODUCT:
    GOOGLE_URL_SHORTENER_API_KEY = ''

# django-compress
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = PRODUCT
if PRODUCT:
    COMPRESS_PRECOMPILERS = (
        ('text/less',
         os.path.join(NODE_MODULES_ROOT, 'less', 'bin',
                      'lessc -x {infile} {outfile}')),
        ('text/coffeescript',
         os.path.join(NODE_MODULES_ROOT, 'coffee-script', 'bin',
                      'coffee --compile -m --stdio')),
    )

# django-google-calendar
if PRODUCT:
    GCAL_CALENDAR_ID = (
        # 本番用Google Calendar
        "",
    )

LOCAL_SETTINGS_LOADED = True

