from kuvaselaamo.settings import *

SECRET_KEY = "xxx"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

DEFAULT_FROM_EMAIL = "kissa@kissa.com"
