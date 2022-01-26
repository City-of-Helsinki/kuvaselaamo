import re
from urllib.parse import urlencode

import responses
from django.urls import reverse

from hkm.finna import FinnaClient
from hkm.tests.mock_finna_responses import (
    FACETS_RESPONSE,
    RECORD_RESPONSE,
    SEARCH_RESPONSE,
)
from hkm.views.views import handler404, handler500


def mock_all_the_responses(mocked_responses, should_fire_all=False):
    mocked_responses.assert_all_requests_are_fired = should_fire_all
    mocked_responses.add(
        responses.GET,
        re.compile(r"^https://api.finna.fi/v1/search.*?[?&]page"),
        json=SEARCH_RESPONSE,
        status=200,
    )

    mocked_responses.add(
        responses.GET,
        re.compile(r"^https://api.finna.fi/v1/search.*?[?&]facet"),
        json=FACETS_RESPONSE,
        status=200,
    )

    mocked_responses.add(
        responses.GET,
        FinnaClient.API_ENDPOINT + "record",
        json=RECORD_RESPONSE,
        status=200,
    )


def test_home_view_renders(client, mocked_responses):
    response = client.get(reverse("hkm_home"))

    assert response.status_code == 200


def test_info_view(client, mocked_responses):
    response = client.get(reverse("hkm_info"))

    assert response.status_code == 200


def test_siteinfo_about_view(client, mocked_responses):
    response = client.get(reverse("hkm_siteinfo_about"))

    assert response.status_code == 200


def test_siteinfo_accessibility_view(client, mocked_responses):
    response = client.get(reverse("hkm_siteinfo_accessibility"))

    assert response.status_code == 200


def test_siteinfo_privacy_view(client, mocked_responses):
    response = client.get(reverse("hkm_siteinfo_privacy"))

    assert response.status_code == 200


def test_siteinfo_qa_view(client, mocked_responses):
    response = client.get(reverse("hkm_siteinfo_QA"))

    assert response.status_code == 200


def test_siteinfo_terms_view(client, mocked_responses):
    response = client.get(reverse("hkm_siteinfo_terms"))

    assert response.status_code == 200


def test_public_collections_view(client, mocked_responses):
    response = client.get(reverse("hkm_public_collections"))

    assert response.status_code == 200


def test_search_view(client, mocked_responses):
    mock_all_the_responses(mocked_responses)

    response = client.get(reverse("hkm_search"))

    assert response.status_code == 200


def test_search_view_with_search(client, mocked_responses):
    mock_all_the_responses(mocked_responses)

    response = client.get(reverse("hkm_search"), {"search": "torni"})

    assert response.status_code == 200


def test_search_record_detail_view(client, mocked_responses):
    mock_all_the_responses(mocked_responses)

    response = client.get(
        reverse("hkm_search_record"), {"image_id": "hkm.HKMS000005:km003mrk"}
    )

    assert response.status_code == 200


def test_legacy_record_detail_view(client, mocked_responses):
    expected_url = reverse("hkm_search_record")
    expected_query = urlencode({"image_id": "hkm.HKMS000005:km003mrk"})

    response = client.get(
        reverse(
            "hkm_legacy_record_details", kwargs={"finna_id": "hkm.HKMS000005:km003mrk"}
        )
    )

    assert response.status_code == 301
    assert response.url == f"{expected_url}?{expected_query}"


def test_handler404(rf):
    request = rf.get("/search/")
    request.session = {}

    response = handler404(request, exception=None)

    assert response.status_code == 404
    assert "404 - Sivua ei löydy" in response.content.decode("utf-8")


def test_handler500(rf):
    request = rf.get("/search/")
    request.session = {}

    response = handler500(request)

    assert response.status_code == 500
    assert "500 - Palvelinvirhe" in response.content.decode("utf-8")
