import io
import logging

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from hkm.models.models import TmpImage

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
    # fetch already saved cropped image
    r = requests.get(order_line.crop_image_url)
    cropped_image = Image.open(io.BytesIO(r.content))
    crop_io = io.BytesIO()
    cropped_image.save(crop_io, format=cropped_image.format)
    filename = f"{title}.{cropped_image.format.lower()}"
    LOG.debug("Cropped image", extra={"data": {"size": repr(cropped_image.size)}})
    crop_file = InMemoryUploadedFile(
        crop_io, None, filename, cropped_image.format, None, None
    )
    tmp_image = TmpImage(record_id=order_line.record_finna_id, edited_image=crop_file)
    tmp_image.save()
    return tmp_image
