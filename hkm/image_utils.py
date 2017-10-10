# -*- coding: utf-8 -*-
import StringIO
import logging

from django.core.files.uploadedfile import InMemoryUploadedFile

from hkm.models.models import TmpImage
from hkm.finna import DEFAULT_CLIENT as FINNA

LOG = logging.getLogger(__name__)


def crop(image, crop_x, crop_y, crop_width, crop_height, img_width, img_height):
    width, height = image.size
    width_multiplier = width / img_width
    height_multiplier = height / img_height
    image_crop_x = crop_x * width_multiplier
    image_crop_y = crop_y * height_multiplier
    image_crop_width = crop_width * width_multiplier
    image_crop_height = crop_height * height_multiplier
    box = (
        int(image_crop_x),
        int(image_crop_y),
        int(image_crop_x) + int(image_crop_width),
        int(image_crop_y) + int(image_crop_height),
    )
    return image.crop(box)


def get_cropped_full_res_file(title, order_line):
    full_res_image = FINNA.download_image(order_line.record_finna_id)
    cropped_image = crop(
        full_res_image,
        order_line.crop_x,
        order_line.crop_y,
        order_line.crop_width,
        order_line.crop_height,
        order_line.original_width,
        order_line.original_height
    )
    crop_io = StringIO.StringIO()
    cropped_image.save(crop_io, format=full_res_image.format)
    filename = u'%s.%s' % (title, full_res_image.format.lower())
    LOG.debug('Cropped image', extra={
              'data': {'size': repr(cropped_image.size)}})
    crop_file = InMemoryUploadedFile(crop_io, None, filename, full_res_image.format, crop_io.len, None)
    tmp_image = TmpImage(record_id=order_line.record_finna_id,
                         edited_image=crop_file)
    tmp_image.save()
    return tmp_image