# -*- coding: utf-8 -*-

import logging

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


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
