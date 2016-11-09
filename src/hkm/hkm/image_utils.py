
# -*- coding: utf-8 -*-

import logging


LOG = logging.getLogger(__name__)


def crop(full_res_image, crop_x, crop_y, crop_width, crop_height, img_width, img_height):
  full_res_width, full_res_height = full_res_image.size
  width_multiplier = full_res_width / img_width
  height_multiplier = full_res_height / img_height
  full_res_crop_x = crop_x * width_multiplier
  full_res_crop_y = crop_y * height_multiplier
  full_res_crop_width = crop_width * width_multiplier
  full_res_crop_height = crop_height * height_multiplier
  box = (
      int(full_res_crop_x),
      int(full_res_crop_y),
      int(full_res_crop_x) + int(full_res_crop_width),
      int(full_res_crop_y) + int(full_res_crop_height),
  )
  LOG.debug('Crop image', extra={'data': {
      'full_res_image': str(full_res_width) + ', ' + str(full_res_height) + ', ' + full_res_image.format,
      'preview_image': str(img_width) + ', ' + str(img_height),
      'scaling_multipliers': str(width_multiplier) + ', ' + str(height_multiplier),
      'crop_options': str(crop_x) + ', ' + str(crop_y) + ', ' + str(crop_width) + ', ' + str(crop_height),
      'scaled_crop_options': str(full_res_crop_x) + ', ' + str(full_res_crop_y) + ', ' + str(full_res_crop_width) + ', ' + str(full_res_crop_height),
      'crop_box': repr(box),
    }})
  return full_res_image.crop(box)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
