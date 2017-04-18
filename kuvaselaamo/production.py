
# -*- coding: utf-8 -*-

#- This file documents what are the settings needed in production
#- The values should not be written here, just documentation what
#- is needed.
#-
#- Infrastructure specific settings in production come from local_settings.py
#- which is importing this file.

from project.settings import *
#from celery.schedules import crontab

# REMEMBER TO MAKE SURE SECRET_KEY IS IN local_settings.py
#SECRET_KEY = 'very secret key'

DEBUG = False
TEMPLATE_DEBUG = False

# Compress
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_HTML = True
# Address celery problems (task #5540)
BROKER_HEARTBEAT = 0

# Django
# TODO Email backend settings

# TODO
HKM_MY_DOMAIN = 'http://kuvaselaamo.haltudemo.fi/'
HKM_FEEDBACK_NOTIFICATION_EMAILS = [
    '',
]
HKM_FEEDBACK_FROM_EMAIL = ''


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
