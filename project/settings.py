
# -*- coding: utf-8 -*-

import os
import djcelery
import logging

djcelery.setup_loader()

BASEDIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASEDIR, 'database.db'),
  }
}

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
  }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

USE_TZ = True
TIME_ZONE = 'Europe/Helsinki'

LANGUAGE_CODE = 'fi'

LANGUAGES = (
  ('fi', 'FI'),
  ('en', 'EN'),
  ('sv', 'SV'),
)

LOCALE_PATHS = (
  os.path.join(BASEDIR, 'locale'),
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

STATICFILES_DIRS = (
  os.path.join(BASEDIR, 'static'),
)

STATIC_ROOT = os.path.join(BASEDIR, '..', 'staticroot')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASEDIR, '..', 'mediaroot')

MEDIA_URL = '/media/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'hkm.middleware.LanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
  {
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASEDIR, 'templates')],
    'OPTIONS': {
      'loaders': (
        'apptemplates.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
      ),
      'context_processors': (
          'django.contrib.auth.context_processors.auth',
          'django.template.context_processors.debug',
          'django.template.context_processors.i18n',
          'django.template.context_processors.media',
          'django.template.context_processors.static',
          'django.contrib.messages.context_processors.messages',
          'django.template.context_processors.request',
      ),
    }
  },
]

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  'compressor.finders.CompressorFinder',
)

INSTALLED_APPS = (
    'hkm',
    'widget_tweaks',

    'phonenumber_field',

    'djcelery',
    'compressor',

    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'django.contrib.admin.apps.SimpleAdminConfig',
)


# Compress
COMPRESS_HTML = False
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_CSS_FILTERS = [
  'compressor.filters.css_default.CssAbsoluteFilter',
  # 'hutils.compressor_filters.ScssFilter',
]

# Workaround for pyScss problems
# https://github.com/Kronuz/pyScss/issues/70
logging.getLogger('scss').addHandler(logging.StreamHandler())

# Django
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'FI'

HKM_MY_DOMAIN = 'http://localhost:3333'
HKM_MY_DOMAIN = 'http://10.0.1.137:3333'
HKM_FEEDBACK_NOTIFICATION_EMAILS = [
    'dummy.address@tld.fi',
]
HKM_FEEDBACK_FROM_EMAIL = 'system@localhost'
HKM_CROPPED_IMAGES_DOWNLOAD_PATH = os.path.join(MEDIA_ROOT, 'download')

# Paybyway
HKM_PBW_API_KEY = ''
HKM_PBW_SECRET_KEY = ''

# Printmotor

HKM_PRINTMOTOR_USERNAME = ''
HKM_PRINTMOTOR_PASSWORD = ''
HKM_PRINTMOTOR_API_KEY = ''

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
