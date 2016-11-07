
# -*- coding: utf-8 -*-

import logging
import random
from django import template
from hkm.finna import DEFAULT_CLIENT as FINNA

LOG = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def finna_image(img_id, w=0, h=0):
  return FINNA.get_image_url(img_id, w=w, h=h)


@register.filter
def finna_default_image_url(img_id):
  return FINNA.get_image_url(img_id)


@register.filter
def display_images(collection):
  ids = list(collection.records.all().values_list('record_id', flat=True))
  record_count = len(ids)
  image_urls = []

  if record_count == 0:
    image_urls.append('/static/hkm/img/collection_default_image.png')
  elif record_count < 3:
    image_urls.append(finna_image(ids[0]))
  else:
    image_urls = []
    for record_id in random.sample(ids, 3):
      image_urls.append(finna_image(record_id))
    return image_urls
  return image_urls


@register.filter
def is_favorite(record, user):
  return record.is_favorite(user)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
