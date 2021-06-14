# -*- coding: utf-8 -*-

import logging
from random import randrange
from decimal import Decimal

from django import template
from django.template.defaultfilters import floatformat
from django.utils import formats
from django.utils.encoding import force_unicode

from hkm.finna import DEFAULT_CLIENT as FINNA
from kuvaselaamo import settings

LOG = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def finna_image(img_id):
    return finna_default_image_url(img_id)


@register.filter
def finna_default_image_url(img_id):
    return FINNA.get_image_url(img_id)

@register.filter
def record_detail(record):
    array_fields = {}
    translated = []

    photographer = record.get('rawData').get('photographer_str_mv', [])
    format = record.get('rawData').get('format', [])
    measures = record.get('rawData').get('measurements', [])

    for type in format:
        translated.append(type.get('translated'))

    array_fields['photographer'] = ", ".join(photographer) if photographer else ""
    array_fields['image_types'] = ', '.join(translated) if translated else ""
    array_fields['measures'] = ', '.join(measures) if measures else ""
    return array_fields

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


@register.filter(is_safe=True)
def localized_decimal(value, arg=-1):
    formatted_value = floatformat(value, arg)
    return force_unicode(formats.localize(Decimal(formatted_value), use_l10n=True))

@register.filter
def front_page_url(collection):
    img_url = ""
    record_count = collection.records.count() if collection else 0

    if not record_count:
        img_url = '/static/hkm/img/front_page_default_image.jpg'
    else:
        records = collection.records.all()
        random_index = randrange(record_count)
        img_url = records[random_index].get_preview_image_absolute_url()

    return img_url

@register.filter
def showcase_collections(showcase):
    albums = showcase.albums.select_related('owner').all().order_by('created')
    return albums
