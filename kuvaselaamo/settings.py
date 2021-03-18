# -*- coding: utf-8 -*-

import logging
import os
import environ

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, ''),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, ''),
    EMAIL_BACKEND=(str, 'django.core.mail.backends.console.EmailBackend'),
    MAIL_MAILGUN_KEY=(str, ""),
    MAIL_MAILGUN_DOMAIN=(str, ""),
    MAIL_MAILGUN_API=(str, ""),
    HKM_DEFAULT_FROM_EMAIL=(str, 'no-reply@hel.fi'),
    HKM_FEEDBACK_NOTIFICATION_EMAILS=(list, ['dummy.address@hel.ninja']),
    HKM_PBW_API_ENDPOINT = (str, ''),
    HKM_PBW_API_KEY = (str, ''),
    HKM_PBW_SECRET_KEY = (str, ''),
    HKM_PRINTMOTOR_USERNAME = (str, ''),
    HKM_PRINTMOTOR_PASSWORD = (str, ''),
    HKM_PRINTMOTOR_API_KEY = (str, ''),
    HKM_PRINTMOTOR_API_ENDPOINT = (str, ''),
    HKM_POSTAL_FEES = (float, 0.0),
    HKM_MY_DOMAIN = (str, 'http://localhost:8080'),
    LOG_LEVEL=(str, 'ERROR'),
    DEFAULT_FILE_STORAGE=(str, "django.core.files.storage.FileSystemStorage"),
    GS_BUCKET_NAME=(str, ""),
    AZURE_ACCOUNT_NAME=(str, ""),
    AZURE_ACCOUNT_KEY=(str, ""),
    AZURE_CONTAINER=(str, ""),
    ENABLE_ANALYTICS=(bool, False),
    PASSWORD_RESET_TIMEOUT_DAYS=(int, 1),
)

DEBUG = env.bool('DEBUG')

ENABLE_ANALYTICS = env.bool('ENABLE_ANALYTICS')

SECRET_KEY = env.str("SECRET_KEY")
if DEBUG and not SECRET_KEY:
    SECRET_KEY = "xxx"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

EMAIL_BACKEND=env.str('EMAIL_BACKEND')
if env("MAIL_MAILGUN_KEY"):
    ANYMAIL = {
        "MAILGUN_API_KEY": env("MAIL_MAILGUN_KEY"),
        "MAILGUN_SENDER_DOMAIN": env("MAIL_MAILGUN_DOMAIN"),
        "MAILGUN_API_URL": env("MAIL_MAILGUN_API"),
    }

BASEDIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

# Set age of cookie to 15 weeks (in seconds).
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 15

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': env.db(),
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

STATIC_ROOT = os.path.join(BASEDIR, '..', 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASEDIR, '..', 'media')
MEDIA_URL = '/media/'

# For staging env, we use Google Cloud Storage
DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE")
if DEFAULT_FILE_STORAGE == "storages.backends.gcloud.GoogleCloudStorage":
    GS_BUCKET_NAME = env("GS_BUCKET_NAME")

    from google.oauth2 import service_account

    GS_FILE_OVERWRITE = False
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        env("STAGING_GCS_BUCKET_CREDENTIALS")
    )
# For prod, it's Azure Storage
elif DEFAULT_FILE_STORAGE == "storages.backends.azure_storage.AzureStorage":
    AZURE_ACCOUNT_NAME = env("AZURE_BUCKET_ACCOUNT_NAME")
    AZURE_ACCOUNT_KEY = env("AZURE_BUCKET_CREDENTIALS")
    AZURE_CONTAINER = env("AZURE_BUCKET_NAME")

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
    'hkm.middleware.BasketMiddleware',
)

ROOT_URLCONF = 'kuvaselaamo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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
                'kuvaselaamo.context_processors.global_settings',
            ),
        }
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'djangobower.finders.BowerFinder',
)

INSTALLED_APPS = (
    'hkm',
    'widget_tweaks',

    'phonenumber_field',

    'compressor',
    'parler',
    'djangobower',

    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'django.contrib.admin.apps.SimpleAdminConfig',

    'anymail',

    'storages'
)

# Bower
BOWER_COMPONENTS_ROOT = os.path.join(BASEDIR, '..', 'components')

BOWER_INSTALLED_APPS = (
    'ckeditor#4.7.1',
)

# Parler
PARLER_DEFAULT_LANGUAGE_CODE = 'fi'

PARLER_LANGUAGES = {
    1: (
        {'code': 'fi',},
        {'code': 'en',},
        {'code': 'sv',},
    ),
    'default': {
        'fallback': 'fi',             # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
    }
}

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

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'FI'

HKM_MY_DOMAIN = env.str('HKM_MY_DOMAIN')
HKM_FEEDBACK_NOTIFICATION_EMAILS = env.list('HKM_FEEDBACK_NOTIFICATION_EMAILS')
DEFAULT_FROM_EMAIL = env.str('HKM_DEFAULT_FROM_EMAIL')
HKM_CROPPED_IMAGES_DOWNLOAD_PATH = os.path.join(MEDIA_ROOT, 'download')

# Paybyway
HKM_PBW_API_ENDPOINT = env.str('HKM_PBW_API_ENDPOINT')
HKM_PBW_API_KEY = env.str('HKM_PBW_API_KEY')
HKM_PBW_SECRET_KEY = env.str('HKM_PBW_SECRET_KEY')

# Printmotor

HKM_PRINTMOTOR_USERNAME = env.str('HKM_PRINTMOTOR_USERNAME')
HKM_PRINTMOTOR_PASSWORD = env.str('HKM_PRINTMOTOR_PASSWORD')
HKM_PRINTMOTOR_API_KEY = env.str('HKM_PRINTMOTOR_API_KEY')
HKM_PRINTMOTOR_API_ENDPOINT = env.str('HKM_PRINTMOTOR_API_ENDPOINT')

# Pricing

HKM_POSTAL_FEES = env.float('HKM_POSTAL_FEES')

MUSEUM_GROUP = 'museum'

WSGI_APPLICATION = "kuvaselaamo.wsgi.application"

LOG_LEVEL = env('LOG_LEVEL')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'filters': {
        'extra_data_filter': {
            '()': 'hkm.log_filters.ExtraDataFilter'
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s %(data)s',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["extra_data_filter"],
            "formatter": "simple"
        }
    },
    "loggers": {
        'hkm.auditlog_signals': {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        '': {
            "handlers": ["console"],
            "level": LOG_LEVEL
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "kuvaselaamo.validators.AlphabeticPasswordValidator",
    },
]

PASSWORD_RESET_TIMEOUT_DAYS = env('PASSWORD_RESET_TIMEOUT_DAYS')
