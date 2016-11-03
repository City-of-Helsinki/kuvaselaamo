
# -*- coding: utf-8 -*-

from project.settings import *

SECRET_KEY = 'foo'

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#CACHES = {
#  'default': {
#    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#    'LOCATION': 'herp-test-cache',
#    'TIMEOUT': 999999,
#    'OPTIONS': {'MAX_ENTRIES': 99999999},
#  }
#}

#CACHES = {
#  'default': {
#    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#    'LOCATION': os.path.join(BASEDIR, '..', 'django_cache'),
#    'TIMEOUT': 999999,
#    'OPTIONS': {'MAX_ENTRIES': 99999999},
#  }
#}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(name)s %(lineno)s %(message)s %(data)s'
        },
    },
    'filters': {
      'default': {
        '()': 'project.logging_helpers.Filter',
      },
    },
    'handlers': {
        'null': {
            'level':'ERROR',
            'class':'logging.NullHandler',
        },
        'console':{
            'class':'logging.StreamHandler',
            'formatter': 'normal',
            'filters': ['default'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'hkm': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'WARNING',
            },
    }
}

# Celery
BROKER_BACKEND = 'memory'
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True

# Compress
COMPRESS_REBUILD_TIMEOUT = 0

# Testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SAUCELABS_USERNAME = ''
SAUCELABS_ACCESS_KEY = ''

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

