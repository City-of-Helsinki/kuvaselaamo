import io
import logging
import math

import requests
from PIL import Image

LOG = logging.getLogger(__name__)


class FinnaClient(object):
    API_ENDPOINT = "https://api.finna.fi/v1/"
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

    def get_full_res_image_url(self, record_id):
        return f"https://finna.fi/Cover/Show?id={record_id}&size=master&index=0"

    def download_image(self, record_id):
        response = requests.get(self.get_full_res_image_url(record_id), stream=True)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            LOG.error(
                "Could not download a full res url",
                extra={"data": {"record_id": record_id}},
            )
            return None

        return Image.open(io.BytesIO(response.content))


DEFAULT_CLIENT = FinnaClient()
