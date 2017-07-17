# -*- coding: utf-8 -*-

import logging

from django import template

from hkm.finna import DEFAULT_CLIENT as FINNA
from kuvaselaamo import settings

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
    records = collection.records.all()
    record_count = records.count()
    image_urls = []

    if record_count == 0:
        image_urls.append('/static/hkm/img/collection_default_image.png')
    elif record_count < 3:
        image_urls.append(records[0].get_preview_image_absolute_url())
    else:
        image_urls = []
        for record in records[:3]:
            image_urls.append(record.get_preview_image_absolute_url())
        return image_urls
    return image_urls


@register.filter
def is_favorite(record, user):
    return record.is_favorite(user)


@register.filter
def is_museum(user):
    return user.groups.filter(name=settings.MUSEUM_GROUP).exists()
