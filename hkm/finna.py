import io
import logging
import math
import urllib.parse

import requests
from PIL import Image

LOG = logging.getLogger(__name__)


class FinnaClient(object):
    API_ENDPOINT = "https://api.finna.fi/v1/"
    DOWNLOAD_ENDPOINT = "https://finna.fi/"
    timeout = 10

    organisation = None
    material_type = None

    def __init__(self, organisation='"0/HKM/"', material_type='"0/Image/"'):
        self.organisation = organisation
        self.material_type = material_type

    def get_facets(self, search_term, language="fi", date_from=None, date_to=None):
        url = FinnaClient.API_ENDPOINT + "search"
        payload = {
            "lookfor": search_term,
            "filter[]": [
                "format:" + self.material_type,
                "building:" + self.organisation,
                'online_boolean:"1"',
            ],
            "limit": 0,
            "lng": language,
            "facet[]": [
                "author_facet",
                "collection",
                "genre_facet",
                "main_date_str",
                "category_str_mv",
            ],
        }
        if date_from or date_to:
            f = date_from if date_from else "*"
            t = date_to if date_to else "*"
            payload["filter[]"].append(f'search_daterange_mv:"[{f} TO {t}]"')
            payload["search_daterange_mv_type"] = "within"

        try:
            r = requests.get(url, params=payload, timeout=self.timeout)
        except requests.exceptions.RequestException:
            LOG.error("Failed to communicate with Finna API", exc_info=True)
            return None
        else:
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                LOG.error(
                    "Failed to communicate with Finna API",
                    exc_info=True,
                    extra={
                        "data": {"status_code": r.status_code, "response": repr(r.text)}
                    },
                )
                return None

        result_data = r.json()
        if "status" not in result_data or result_data["status"] != "OK":
            LOG.error(
                "Finna query was not successful",
                extra={"data": {"result_data": repr(result_data)}},
            )
            return None

        LOG.debug(
            "Got facet result from Finna",
            extra={"data": {"result_data": repr(result_data)}},
        )
        return result_data

    def search(
        self, search_term, facets=None, page=1, limit=20, language="fi", detailed=False
    ):
        url = FinnaClient.API_ENDPOINT + "search"
        payload = {
            "lookfor": search_term,
            "filter[]": [
                "format:" + self.material_type,
                "building:" + self.organisation,
                'online_boolean:"1"',
            ],
            "page": page,
            "limit": limit,
            "lng": language,
        }

        if facets:
            # Idea is to OR parameters within facet scope and AND facet filters with each other
            # Like this: (Authors A OR B) AND year 1920
            # However this code uses OR in all facets and this seems to work in
            # desired way
            for facet_type, facet_values in facets.items():
                if facet_type == "search_daterange_mv":
                    # Value needs to be inside double quotes, insert value manually to make sure its correct.
                    payload["filter[]"].append(f'search_daterange_mv:"{facet_values}"')
                    payload["search_daterange_mv_type"] = "within"
                else:
                    for facet_value in facet_values:
                        payload["filter[]"].append("~" + facet_type + ":" + facet_value)

        if detailed:
            payload["field[]"] = [
                "id",
                "authors",
                "buildings",
                "formats",
                "genres",
                "humanReadablePublicationDates",
                "imageRights",
                "images",
                "institutions",
                "languages",
                "originalLanguages",
                "presenters",
                "publicationDates",
                "rating",
                "series",
                "subjects",
                "summary",
                "title",
                "year",
                "rawData",
                "imagesExtended",
            ]

        result_data = self._get_finna_result(url, payload)

        LOG.debug(
            "Got search result from Finna",
            extra={"data": {"result_data": repr(result_data)}},
        )

        if not result_data:
            return None

        if limit > 0:
            pages = int(math.ceil(result_data["resultCount"] / float(limit)))
        else:
            pages = 1
        result_data["pages"] = pages
        result_data["limit"] = limit
        result_data["page"] = page
        if page > 1:
            result_data["previous_page"] = page - 1
        else:
            result_data["previous_page"] = None
        if page < pages:
            result_data["next_page"] = page + 1
        else:
            result_data["next_page"] = None
        return result_data

    def get_record(self, record_id):
        if record_id is None:
            LOG.warning("Record id was None, cannot call Finna")
            return None

        url = FinnaClient.API_ENDPOINT + "record"
        payload = {
            "id[]": record_id,
            "field[]": [
                "id",
                "authors",
                "buildings",
                "formats",
                "genres",
                "humanReadablePublicationDates",
                "imageRights",
                "images",
                "institutions",
                "languages",
                "originalLanguages",
                "presenters",
                "publicationDates",
                "rating",
                "series",
                "subjects",
                "summary",
                "title",
                "year",
                "rawData",
                "imagesExtended",
            ],
        }

        result_data = self._get_finna_result(url, payload)

        LOG.debug(
            "Got record result from Finna",
            extra={"data": {"result_data": repr(result_data)}},
        )

        return result_data

    def _get_finna_result(self, url, payload):
        try:
            response = requests.get(url, params=payload, timeout=self.timeout)
        except requests.exceptions.RequestException:
            LOG.error("Failed to communicate with Finna API", exc_info=True)
            return None
        else:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                LOG.error(
                    "Failed to communicate with Finna API",
                    exc_info=True,
                    extra={
                        "data": {
                            "status_code": response.status_code,
                            "response": repr(response.text),
                        }
                    },
                )
                return None

        result_data = response.json()
        if "status" not in result_data or result_data["status"] != "OK":
            LOG.error(
                "Finna query was not successful",
                extra={"data": {"result_data": repr(result_data)}},
            )
            return None

        return result_data

    def get_image_url(self, record_id):
        return f"https://finna.fi/Cover/Show?id={record_id}&fullres=1&index=0"

    def get_full_res_image_url(self, record):
        # attempt to find high resolution original photo url
        if high_resolution_original := self.get_labeled_high_resolution_url(record, "original"):
            return high_resolution_original

        # attempt to find high resolution master photo url
        if high_resolution_master := self.get_labeled_high_resolution_url(record, "master"):
            return high_resolution_master

        # attempt to find original photo urls
        if original := self.get_labeled_image_url(record, "original"):
            return original

        # attempt to find large photo urls
        if large := self.get_labeled_image_url(record, "large"):
            return large

        # fallback previous default implementation if extended image properties not found.
        return f"https://finna.fi/Cover/Show?id={record['id']}&size=master&index=0"

    def download_image(self, record):
        response = requests.get(self.get_full_res_image_url(record), stream=True)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            LOG.error(
                "Could not download a full res url",
                extra={"data": {"record_id": record["id"]}},
            )
            return None

        return Image.open(io.BytesIO(response.content))

    def get_labeled_image_url(self, record, label):
        images_extended = record.get("imagesExtended")
        if not images_extended:
            return None

        for image_extended in images_extended:
            if urls := image_extended.get("urls"):
                if original := urls.get(label):
                    if urllib.parse.urlparse(original).netloc:
                        return original
                    return urllib.parse.urljoin(FinnaClient.DOWNLOAD_ENDPOINT, original)

    def get_labeled_high_resolution_url(self, record, label):
        images_extended = record.get("imagesExtended")
        if not images_extended:
            return None

        for image_extended in images_extended:
            high_resolution = image_extended.get("highResolution")
            if not high_resolution:
                continue

            items = high_resolution.get(label)
            if not items:
                continue

            for item in items:
                params = item.get("params")
                if not params:
                    continue
                return f"{FinnaClient.DOWNLOAD_ENDPOINT}record/DownloadFile?{urllib.parse.urlencode(params)}"

        return None


DEFAULT_CLIENT = FinnaClient()
