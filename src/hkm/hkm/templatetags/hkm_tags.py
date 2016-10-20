
# -*- coding: utf-8 -*-

import logging
from django import template

LOG = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def finna_image(img_id, w=400, h=400):
  url = 'https://finna.fi/Cover/Show?id=%s&w=%d&h=%d' % (img_id, w, h)
  return url




# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
