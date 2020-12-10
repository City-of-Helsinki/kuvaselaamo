# -*- coding: utf-8 -*-

import logging
import math
import urllib
import urlparse
from StringIO import StringIO

import requests
from PIL import Image
from django.core.cache import cache


LOG = logging.getLogger(__name__)


class FinnaClient(object):
    API_ENDPOINT = 'https://api.finna.fi/v1/'
    timeout = 10

    organisation = None
    material_type = None

    def __init__(self, organisation='"0/HKM/"', material_type='"0/Image/"'):
        self.organisation = organisation
        self.material_type = material_type

    def search(self, search_term, page=1, limit=20, language='fi', detailed=False):
        url = FinnaClient.API_ENDPOINT + 'search'
        payload = {
            'lookfor': search_term,
            'filter[]': ['format:' + self.material_type, 'building:' + self.organisation, 'online_boolean:"1"', ],
            'page': page,
            'limit': limit,
            'lng': language,
        }

        if detailed:
            payload['field[]'] = ['id', 'authors', 'buildings', 'formats', 'genres', 'humanReadablePublicationDates',
                                  'imageRights', 'images', 'institutions', 'languages', 'originalLanguages', 'presenters',
                                  'publicationDates', 'rating', 'series', 'subjects', 'summary', 'title', 'year', 'rawData', ]

        try:
            r = requests.get(url, params=payload, timeout=self.timeout)
        except requests.exceptions.RequestException:
            LOG.error('Failed to communicate with Finna API', exc_info=True)
            return None
        else:
            try:
                r.raise_for_status()
                # raise requests.exceptions.HTTPError()
            except requests.exceptions.HTTPError:
                LOG.error('Failed to communicate with Finna API', exc_info=True,
                          extra={'data': {'status_code': r.status_code, 'response': repr(r.text)}})
                return None

        result_data = r.json()
        if not 'status' in result_data or result_data['status'] != 'OK':
            LOG.error('Finna query was not succesfull', extra={
                      'data': {'result_data': repr(result_data)}})
            return None

        LOG.debug('Got result from Finna', extra={
                  'data': {'result_data': repr(result_data)}})
        if limit > 0:
            pages = int(math.ceil(result_data['resultCount'] / float(limit)))
        else:
            pages = 1
        result_data['pages'] = pages
        result_data['limit'] = limit
        result_data['page'] = page
        if page > 1:
            result_data['previous_page'] = page - 1
        else:
            result_data['previous_page'] = None
        if page < pages:
            result_data['next_page'] = page + 1
        else:
            result_data['next_page'] = None
        return result_data

    def get_record(self, record_id):
        url = FinnaClient.API_ENDPOINT + 'record'
        payload = {
            'id[]': record_id,
            'field[]': ['id', 'authors', 'buildings', 'formats', 'genres', 'humanReadablePublicationDates',
                        'imageRights', 'images', 'institutions', 'languages', 'originalLanguages', 'presenters',
                        'publicationDates', 'rating', 'series', 'subjects', 'summary', 'title', 'year', 'rawData', ],
        }
        try:
            r = requests.get(url, params=payload, timeout=self.timeout)
        except requests.exceptions.RequestException:
            LOG.error('Failed to communicate with Finna API', exc_info=True)
            return None
        else:
            try:
                r.raise_for_status()
                # raise requests.exceptions.HTTPError()
            except requests.exceptions.HTTPError:
                LOG.error('Failed to communicate with Finna API', exc_info=True,
                          extra={'data': {'status_code': r.status_code, 'response': repr(r.text)}})
                return None

        result_data = r.json()
        if not 'status' in result_data or result_data['status'] != 'OK':
            LOG.error('Finna query was not succesfull', extra={
                      'data': {'result_data': repr(result_data)}})
            return None

        LOG.debug('Got result from Finna', extra={
                  'data': {'result_data': repr(result_data)}})
        return result_data

    def get_image_url(self, record_id, w=0, h=0):
        if w != 0 and h != 0:
            url = 'https://finna.fi/Cover/Show?id=%s&w=%d&h=%d' % (
                record_id, w, h)
        else:
            url = 'https://finna.fi/Cover/Show?id=%s&fullres=1&index=0' % record_id
        return url

    def get_full_res_image_url(self, preview_image_url):
        timeout = 6

        """
        HKM image server responds with 200 text body response if there is no full res version for the
        image. This checks the response headers to find out whether full res image exists or not and
        returns the full res image url if it does. Else returns None
        """
        cache_key = 'hkm_%s' % preview_image_url
        cached_value = cache.get(cache_key)
        if cached_value:
            return cached_value

        url_components = urlparse.urlparse(preview_image_url)
        qs_params = dict(urlparse.parse_qsl(url_components.query))
        qs_params['dataType'] = 'org'

        url_components = list(url_components)
        url_components[4] = urllib.urlencode(qs_params)
        url = urlparse.urlunparse(url_components)
        try:
            r = requests.head(url, timeout=self.timeout)
        except requests.exceptions.RequestException:
            LOG.error('Failed to communicate with FINNA image server',
                      exc_info=True)
            # Cache negative result for an hour
            cache.set(cache_key, None, 3600)
            return None
        else:
            try:
                r.raise_for_status()
                # raise requests.exceptions.HTTPError()
            except requests.exceptions.HTTPError:
                LOG.error('Failed to communicate with FINNA image server', exc_info=True,
                          extra={'data': {'status_code': r.status_code, 'response': repr(r.text)}})
                # Cache negative result for an hour
                cache.set(cache_key, None, 3600)
                return None

        LOG.debug('Got result from FINNA image server',
                  extra={'data': {'url': url, 'result_headers': repr(r.headers)}})
        try:
            content_type = r.headers['content-type']
            if 'image' in content_type:
                # Cache positive result for a week
                cache.set(cache_key, url, 7 * 24 * 3600)
                return url
        except KeyError:
            pass

        cache.set(cache_key, None, 3600)
        return None

    def download_image(self, record_id):
        r = requests.get(self.get_image_url(record_id), stream=True)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException:
            LOG.error('Could not download a full res url',
                      extra={'data': {'record_id': record_id}})
        else:
            return Image.open(StringIO(r.content))
        return None


DEFAULT_CLIENT = FinnaClient()

