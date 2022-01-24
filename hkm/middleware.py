import logging

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import LANGUAGE_SESSION_KEY

LOG = logging.getLogger(__name__)


class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if LANGUAGE_SESSION_KEY not in request.session:
            if request.user.is_authenticated:
                language = request.user.profile.language
                request.session[LANGUAGE_SESSION_KEY] = language
            else:
                request.session[LANGUAGE_SESSION_KEY] = settings.LANGUAGE_CODE
            return None
