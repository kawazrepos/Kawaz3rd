"""
Django settings for Kawaz project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import sys

REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add extra PYTHON_PATH
LIB = os.path.join(REPOSITORY_ROOT, 'src', 'lib')
sys.path.insert(0, os.path.join(LIB, 'django-activities'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xd(wr812awpkuu4+7o)#ugb)*a0z!-m^an+m)%ly$l(ses8_g1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

SITE_ID = 1

ROOT_URLCONF = 'kawaz.urls'
WSGI_APPLICATION = 'kawaz.wsgi.application'
AUTH_USER_MODEL = 'personas.Persona'

TEST_RUNNER = 'kawaz.core.tests.runner.KawazDiscoverRunner'
TESTING = False


# Application definition
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
    'debug_toolbar',
    'thumbnailfield',
    'roughpages',
    'registration',
    'crispy_forms',
    'compressor',
    'activities',
    'kawaz.core.management',
    'kawaz.core.db',
    'kawaz.core.comments',
    'kawaz.core.utils',
    'kawaz.core.personas',
    'kawaz.core.publishments',
    'kawaz.core.registrations',
    'kawaz.core.forms',
    'kawaz.core.templatetags',
    'kawaz.core.gcal',
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

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'roughpages.middleware.RoughpageFallbackMiddleware',
)

CACHES = {
    'default': {
        # 開発用にダミーキャッシュを指定
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
from django.utils.translation import ugettext_lazy as _
USE_I18N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('ja', _('Japanese')),
)

USE_L10N = True
LOCALE_PATHS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'locale'),
)

USE_TZ = True
TIME_ZONE = 'Asia/Tokyo'


# Template
TEMPLATE_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

MEDIA_URL = '/storage/'
MEDIA_ROOT = os.path.join(REPOSITORY_ROOT, 'public', 'storage')

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
FIXTURE_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'fixtures',),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
    }
}
# validation_on_save decorator (kawaz.core.db.decorators)
# To disable automatical validation, set this variable to False
VALIDATE_ON_SAVE_DISABLE = False


# kawaz.core.personas
# 使用可能なユーザー名の正規表現
PERSONAS_VALID_USERNAME_PATTERN = r"^[\w\-\_]+$"
# 使用不可なユーザー名（URLルールなどにより）
PERSONAS_INVALID_USERNAMES = (
    'my',
)


# django-thumbnailfield
THUMBNAIL_SIZE_PATTERNS = {
    'huge': (288, 288,),
    'large': (96, 96,),
    'middle': (48, 48,),
    'small': (24, 24,),
}
PRODUCT_THUMBNAIL_SIZE_PATTERNS = {
    'huge': (512, 288,),
    'large': (172, 96,),
    'middle': (86, 48,),
    'small': (43, 24,),
}
ADVERTISEMENT_IMAGE_SIZE_PATTERNS = {
    'huge': (512, 288,),
    'large': (172, 96,),
    'middle': (86, 48,),
    'small': (43, 24,),
}
SCREENSHOT_IMAGE_SIZE_PATTERNS = {
    None: (32, 32),
}

# django-permission
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'permission.backends.PermissionBackend',
)
# Permission presence check in DEBUG mode
# from django-permission 0.5.3
PERMISSION_CHECK_PERMISSION_PRESENCE = DEBUG


# django-inspectional-registration
REGISTRATION_SUPPLEMENT_CLASS = (
    'kawaz.core.registrations.models.RegistrationSupplement')
REGISTRATION_NOTIFICATION = True
REGISTRATION_NOTIFICATION_ADMINS = True
REGISTRATION_NOTIFICATION_RECIPIENTS = (

)


ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_DJANGO_AUTH_URLS_ENABLE = False
LOGIN_URL = '/registration/login/'
LOGOUT_URL = '/registration/logout/'
LOGIN_REDIRECT_URL = '/'


# django-compressor
COMPRESS_ENABLED = not DEBUG
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
from activities.notifiers.registry import registry
from activities.notifiers.oauth.twitter import TwitterActivityNotifier
ACTIVITIES_NOTIFIER_CONFIG_ROOT = os.path.join(
    REPOSITORY_ROOT, 'config', 'activities', 'notifiers',
) 
registry.register(TwitterActivityNotifier(
    TwitterActivityNotifier.get_credentials(os.path.join(
        ACTIVITIES_NOTIFIER_CONFIG_ROOT,
        'credentials_twitter_kawaz_test.json'
    ))
), 'twitter_kawaz_official')
registry.register(TwitterActivityNotifier(
    TwitterActivityNotifier.get_credentials(os.path.join(
        ACTIVITIES_NOTIFIER_CONFIG_ROOT,
        'credentials_twitter_kawazinfo_test.json'
    ))
), 'twitter_kawaz_info')
ACTIVITIES_DEFAULT_NOTIFIERS = (
    'twitter_kawaz_official',
    'twitter_kawaz_info',
)
del registry
del TwitterActivityNotifier

# kawaz.apps.activities.contrib.hatenablog
ACTIVITIES_HATENABLOG_FEED_URL = 'http://kawazinfo.hateblo.jp/rss'

# kawaz.apps.events.gcal
GCAL_CALENDAR_ID = (
    # DEBUG用カレンダー
    'kawaz.org_u41faouova38rcoh8eaimbg42c@group.calendar.google.com'
)
GCAL_EVENT_MODEL = 'events.Event'
GCAL_BACKEND_CLASS = 'kawaz.apps.events.gcal.KawazGoogleCalendarBackend'
GCAL_CLIENT_SECRETS = os.path.join(
    REPOSITORY_ROOT, 'config', 'gcal', 'client_secrets.json')
GCAL_CREDENTIALS = os.path.join(
    REPOSITORY_ROOT, 'config', 'gcal', 'credentials.json')

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

if DEBUG:
    # テスト時のRuntimeWarningをexceptionにしている
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

# 環境依存の設定（デプロイサーバー固有の設定など）を読み込む
LOCAL_SETTINGS_LOADED = False
try:
    from .local_settings import *
except ImportError:
    pass
