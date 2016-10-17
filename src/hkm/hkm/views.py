
# -*- coding: utf-8 -*-

import logging
from django.views.generic import TemplateView

LOG = logging.getLogger(__name__)


class IndexView(TemplateView):
  template_name = 'hkm/views/index.html'


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
