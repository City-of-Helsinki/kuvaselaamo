
# -*- coding: utf-8 -*-

import logging
from django.utils.translation import LANGUAGE_SESSION_KEY
from hkm import settings

LOG = logging.getLogger(__name__)


class LanguageMiddleware(object):
  def process_request(self, request):
    if not LANGUAGE_SESSION_KEY in request.session:
      if request.user.is_authenticated():
        language = request.user.profile.language
        request.session[LANGUAGE_SESSION_KEY] = language
      else:
        request.session[LANGUAGE_SESSION_KEY] = settings.DEFAULT_LANGUAGE
      return None


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
