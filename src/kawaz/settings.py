"""
Django settings for Kawaz project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xd(wr812awpkuu4+7o)#ugb)*a0z!-m^an+m)%ly$l(ses8_g1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tastypie',
    'permission',
    'thumbnailfield',
    'kawaz.core.db',
    'kawaz.core.personas',
    'kawaz.core.permissions',
    'kawaz.apps.announcements',
    'kawaz.apps.profiles',
    'kawaz.apps.projects',
    'kawaz.apps.events',
    'kawaz.apps.blogs',
    'kawaz.apps.products',
    'kawaz.apps.stars',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'permission.backends.PermissionBackend',
)

ROOT_URLCONF = 'kawaz.urls'

WSGI_APPLICATION = 'kawaz.wsgi.application'

# validation_on_save decorator (kawaz.core.db.decorators)
# To disable automatical validation, set this variable to False
VALIDATE_ON_SAVE_DISABLE = False

AUTH_USER_MODEL = 'personas.Persona'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
    }
}

THUMBNAIL_SIZE_PATTERNS = {
    'huge': (288, 288,),
    'large': (96, 96,),
    'middle': (48, 48,),
    'small': (24, 24,),
}

ADVERTISEMENT_IMAGE_SIZE_PATTERNS = {
    None : (None, None,),
}

SCREENSHOT_IMAGE_SIZE_PATTERNS = {
    None : (None, None,),
}

# Permission presence check in DEBUG mode
# from django-permission 0.5.3
PERMISSION_CHECK_PERMISSION_PRESENCE = DEBUG

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

MEDIA_ROOT = os.path.abspath(os.path.join(REPOSITORY_ROOT, 'storage'))
MEDIA_URL = '/storage/'

TEMPLATE_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'kawaz', 'templates'),
)

LOGIN_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/statics/'

STATICFILES_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'kawaz', 'statics'),
)

# tastypie

TASTYPIE_DEFAULT_FORMATS = ['json',]
