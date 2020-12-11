# -*- coding: utf-8 -*-

import logging
import math
import urllib
import urlparse
from StringIO import StringIO

import requests
from PIL import Image


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

    # This will return fullres image url if w and h == 0
    def get_image_url(self, record_id, w=0, h=0):
        if w != 0 and h != 0:
            url = 'https://finna.fi/Cover/Show?id=%s&w=%d&h=%d' % (
                record_id, w, h)
        else:
            url = 'https://finna.fi/Cover/Show?id=%s&fullres=1&index=0' % record_id
        return url

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

