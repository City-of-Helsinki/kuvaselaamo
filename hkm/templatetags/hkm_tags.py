import logging
from random import randrange
from urllib.parse import urlencode

from django import template
from django.utils.safestring import mark_safe

from hkm.finna import DEFAULT_CLIENT as FINNA

LOG = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def finna_image(img_id):
    return finna_default_image_url(img_id)


@register.simple_tag
def finna_thumbnail(record):
    return FINNA.get_thumbnail_image_url(record)


@register.filter
def truncate_description(value):
    result = value.removeprefix("sisällön kuvaus: ")
    result = result.removesuffix("mustavalkoinen")
    result = result.removesuffix("värillinen")
    return result


@register.filter
def truncate_era(value):
    result = value.removeprefix("kuvausaika: ")
    return result.removeprefix("kuvausaika ")


@register.filter
def truncate_geographic(value):
    return value.replace("Pohjoismaat, Suomi, Uusimaa, ", "")


@register.filter(is_safe=True)
def decorate_license(value):
    license_links = {"CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.fi"}

    if license_link := license_links.get(value):
        return mark_safe(f"<a href='{license_link}' target='_blank'>{value}</a>")
    return value


@register.filter
def finna_default_image_url(img_id):
    return FINNA.get_image_url(img_id)


@register.filter
def record_detail(record):
    array_fields = {}
    translated = []

    photographer = record.get("rawData").get("photographer_str_mv", [])
    format = record.get("rawData").get("format", [])
    measures = record.get("rawData").get("measurements", [])

    for data in format:
        if isinstance(data, dict):
            translated.append(data.get("translated"))

    array_fields["photographer"] = ", ".join(photographer) if photographer else ""
    array_fields["image_types"] = ", ".join(translated) if translated else ""
    array_fields["measures"] = ", ".join(measures) if measures else ""
    return array_fields


@register.filter
def display_images(collection):
    records = collection.records.all()
    record_count = records.count()
    image_urls = []

    if record_count == 0:
        image_urls.append("/static/hkm/img/collection_default_image.png")
    elif record_count < 3:
        image_urls.append(records[0].get_thumbnail_image_absolute_url())
    else:
        image_urls = []
        for record in records[:3]:
            image_urls.append(record.get_thumbnail_image_absolute_url())
        return image_urls
    return image_urls


@register.filter
def front_page_url(collection):
    img_url = ""
    record_count = collection.records.count() if collection else 0

    if not record_count:
        img_url = "/static/hkm/img/front_page_default_image.jpg"
    else:
        records = collection.records.all()
        random_index = randrange(record_count)
        img_url = records[random_index].get_preview_image_absolute_url()

    return img_url


@register.filter
def showcase_collections(showcase):
    albums = showcase.albums.select_related("owner").all().order_by("created")
    return albums


@register.filter
def search_keywords(url_params):
    keywords = []
    ignored_params = ["date_from", "date_to", "page"]

    for key, value in url_params.items():
        if key in ignored_params or len(value) == 0:
            continue

        if isinstance(value, list):
            for item in value:
                keywords.append({"value": item, "facet_type": key})
        else:
            keywords.append({"value": value, "facet_type": key})

    # Manually check date_from and date_to to combine them into one keyword
    date_from = url_params.get("date_from", "")
    date_to = url_params.get("date_to", "")

    if date_from or date_to:
        combined = f"{date_from} - {date_to}"
        keywords.append({"value": combined, "facet_type": "date_range"})

    return keywords


@register.filter()
def return_link(url_params):
    cleaned_params = {}

    for key, value in url_params.items():
        if value:
            cleaned_params[key] = value

    encoded_params = urlencode(cleaned_params, doseq=True)
    return f"?{encoded_params}" if encoded_params else ""


@register.filter()
def record_index(record, search_result):
    records_in_sr = search_result.get("records", [])

    record_in_sr = next((x for x in records_in_sr if x["id"] == record.get("id")), None)

    index = records_in_sr.index(record_in_sr) + 1
    return f"{index} / {search_result.get('resultCount')}"
