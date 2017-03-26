###############################################################################
#
#   Kawaz ポータルサイトの設定
#
###############################################################################
from .pre_settings import *
from django.utils.translation import ugettext_lazy as _

# セッション暗号化用文字列の指定
SECRET_KEY = 'ここに十分に長いランダムな文字列'

# 開発モードを指定
DEBUG = True
PRODUCT = False

# アクティブなサイトIDを指定
SITE_ID = 1

# 利用しているアプリ
INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_comments',
    'rest_framework',
    'permission',
    'registration.contrib.notification',
    'debug_toolbar',
    'vcs_info_panel',
    'thumbnailfield',
    'roughpages',
    'registration',
    'crispy_forms',
    'compressor',
    'activities',
    'slack_invitation',
    'google_calendar',
    'kawaz.core.management',
    'kawaz.core.db',
    'kawaz.core.comments',
    'kawaz.core.utils',
    'kawaz.core.personas',
    'kawaz.core.publishments',
    'kawaz.core.registrations',
    'kawaz.core.forms',
    'kawaz.core.templatetags',
    'kawaz.core.activities.hatenablog',
    'kawaz.apps.announcements',
    'kawaz.apps.attachments',
    'kawaz.apps.projects',
    'kawaz.apps.events',
    'kawaz.apps.blogs',
    'kawaz.apps.products',
    'kawaz.apps.stars',
    'kawaz.apps.kfm',
)

# 利用しているミドルウェア
MIDDLEWARE_CLASSES = (
    'kawaz.core.middlewares.exception.UserBasedExceptionMiddleware',
    # UserBasedExceptionは例外を補足し詳細なエラーレポートを返すので先頭
    # で定義する必要がある（例外処理は応答フェーズなので逆順実行なため）
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'roughpages.middleware.RoughpageFallbackMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'builtins': [
                'permission.templatetags.permissionif',
                'kawaz.core.templatetags.templatetags.expr',
                'kawaz.apps.kfm.templatetags.kfm',
            ],
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(REPOSITORY_ROOT, 'src', 'templates'),
        ]
    },
]

# データベースの設定
DATABASES = {
    'default': {
        # 開発用にSQLite3を利用
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
    }
}

# キャッシュシステムの設定
CACHES = {
    'default': {
        # 開発用にローカルキャッシュを使用する
        # セッション情報の保持にキャッシュシステムを使用しているため
        # ダミーキャッシュは使用できない
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'this value should be quite unique for Kawaz cache',
    }
}

# djangoのセッション情報をキャッシュおよびDBに保存
# デフォルトはDB保存なので、これにより体感可能なレベルでの高速化が可能
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# 静的ファイルの設定
STATIC_URL = '/statics/'
STATIC_ROOT = os.path.join(REPOSITORY_ROOT, 'public', 'statics')
STATICFILES_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'statics'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# アップロードファイルの設定
MEDIA_URL = '/storage/'
MEDIA_ROOT = os.path.join(REPOSITORY_ROOT, 'public', 'storage')

# 初期データ・デバッグ情報の設定
FIXTURE_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'fixtures',),
)

# テスト関係の設定
TEST_RUNNER = 'kawaz.core.tests.runner.KawazDiscoverRunner'
TESTING = False

ROOT_URLCONF = 'kawaz.urls'
WSGI_APPLICATION = 'kawaz.wsgi.application'

# 認証関係の設定
AUTH_USER_MODEL = 'personas.Persona'
LOGIN_URL = '/registration/login/'
LOGOUT_URL = '/registration/logout/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_BACKEND_CLASS = 'kawaz.core.registrations.backends.KawazRegistrationBackend'

# 国際化の設定
USE_TZ = True
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('ja', _('Japanese')),
)
LOCALE_PATHS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'locale'),
)

# loggerの設定
LOG_BASE_DIR = '/var/log'

if PRODUCT:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOG_BASE_DIR, 'org.kawaz.warning.log'),
                'formatter': 'verbose'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins',],
                'level': 'ERROR',
                'propagate': False,
            },
            'kawaz.core.utils': {
                'handlers': ['file',],
                'level': 'ERROR',
            }
        }
    }

# プラグインの設定 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# django-thumbnailfield
THUMBNAIL_SIZE_PATTERNS = {
    'huge': (288, 288,),
    'large': (96, 96,),
    'middle': (48, 48,),
    'small': (24, 24,),
    'grayscale': ((96, 96, 'thumbnail'), (None, None, 'grayscale')),
}

# django-permission
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'permission.backends.PermissionBackend',
)
# 指定されたパーミッションが存在するかどうかテストを行う
PERMISSION_CHECK_PERMISSION_PRESENCE = True

# django-inspectional-registration
REGISTRATION_SUPPLEMENT_CLASS = (
    'kawaz.core.registrations.models.RegistrationSupplement')
REGISTRATION_NOTIFICATION = True
REGISTRATION_NOTIFICATION_ADMINS = True
REGISTRATION_NOTIFICATION_RECIPIENTS = (
    'webmaster@kawaz.org',
)
REGISTRATION_DJANGO_AUTH_URLS_ENABLE = False

# django-compressor
COMPRESS_OUTPUT_DIR = ''
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
)

# django-rest-framework
DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

# django-activities
ACTIVITIES_ENABLE_NOTIFICATION = True
ACTIVITIES_ENABLE_OAUTH_NOTIFICATION = True
ACTIVITIES_ENABLE_HIPCHAT_NOTIFICATION = False
ACTIVITIES_ENABLE_SLACK_NOTIFICATION = True
ACTIVITIES_INSTALLED_NOTIFIERS = (
    ('twitter_kawaz_official',
     'activities.notifiers.oauth.twitter.TwitterActivityNotifier',
     os.path.join(CONFIG_ROOT, 'activities', 'notifiers',
                  'credentials_twitter_kawaz_test.json')),
    ('twitter_kawaz_info',
     'activities.notifiers.oauth.twitter.TwitterActivityNotifier',
     os.path.join(CONFIG_ROOT, 'activities', 'notifiers',
                  'credentials_twitter_kawazinfo_test.json')),
)
ACTIVITIES_DEFAULT_NOTIFIERS = (
    'twitter_kawaz_info',
)

ACTIVITIES_TEMPLATE_EXTENSIONS = {
    'twitter': '.txt',
    'slack': '.txt',
}

# kawaz.apps.activities.contrib.hatenablog
ACTIVITIES_HATENABLOG_FEED_URL = 'http://kawazinfo.hateblo.jp/rss'

# django-google-calendar
GOOGLE_CALENDAR_CALENDAR_ID = (
    # DEBUG用カレンダー
    'kawaz.org_u41faouova38rcoh8eaimbg42c@group.calendar.google.com'
)
GOOGLE_CALENDAR_EVENT_MODEL = 'events.Event'
GOOGLE_CALENDAR_BACKEND_CLASS = (
    'kawaz.apps.events.gcal.KawazGoogleCalendarBackend'
)
GOOGLE_CALENDAR_CLIENT_SECRETS = os.path.join(CONFIG_ROOT,
                                              'gcal', 'client_secrets.json')
GOOGLE_CALENDAR_CREDENTIALS = os.path.join(CONFIG_ROOT,
                                           'gcal', 'credentials.json')
GOOGLE_CALENDAR_ENABLE_NOTIFICATIONS = True

# django_comments
COMMENTS_APP = 'kawaz.core.comments'
COMMENTS_HIDE_REMOVED = False

# crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap3', 'crispy')

# django-suit
SUIT_CONFIG = dict(
    ADMIN_NAME='Kawaz',
    SEARCH_URL='/central-dogma/personas/persona/',
)


# django-debug-toolbar
def show_debug_toolbar(request):
    from django.conf import settings
    if settings.TESTING:
        return False
    if not request.is_ajax() and request.user and request.user.is_superuser:
        return True
    return settings.DEBUG

DEBUG_TOOLBAR_PATCH_SETTINGS = True
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'kawaz.settings.show_debug_toolbar',
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'vcs_info_panel.panels.GitInfoPanel'
]

# 雑多な設定 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Timezone関連のRuntimeWarningをexceptionにしている
# https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#code
import warnings
warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')

# DjangoのMessageをBootstrap3に適応させている
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# 神、いわゆるゴッド
GEEKDRUMS_NAME = 'miio'

# 環境依存の設定（デプロイサーバー固有の設定など）を読み込む
LOCAL_SETTINGS_LOADED = False
try:
    from .local_settings import *
except ImportError:
    pass
