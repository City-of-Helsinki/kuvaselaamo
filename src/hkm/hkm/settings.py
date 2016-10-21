
# -*- coding: utf-8 -*-

from django.conf import settings

SAUCELABS_USERNAME = getattr(settings, 'SAUCELABS_USERNAME', '')
SAUCELABS_ACCESS_KEY = getattr(settings, 'SAUCELABS_ACCESS_KEY', '')

DEFAULT_LANGUAGE = settings.LANGUAGE_CODE

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

