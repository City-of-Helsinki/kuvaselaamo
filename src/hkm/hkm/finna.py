
# -*- coding: utf-8 -*-

import math
import logging
import requests

LOG = logging.getLogger(__name__)


class FinnaClient(object):
  API_ENDPOINT = 'https://api.finna.fi/v1/'
  timeout = 10

  organisation = None
  material_type = None

  def __init__(self, organisation='"0/HKM/"', material_type='"0/Image/"'):
    self.organisation = organisation
    self.material_type = material_type

  def get_facets(self, search_term, language='fi'):
    url = FinnaClient.API_ENDPOINT + 'search'
    payload = {
      'lookfor': search_term,
      'filter[]': ['format:'+self.material_type, 'building:'+self.organisation, 'online_boolean:"1"'],
      'limit': 0,
      'lng': language,
      'facet[]': ['author_facet', 'collection', 'genre_facet', 'main_date_str', 'category_str_mv']
    }
    try:
      r = requests.get(url, params=payload, timeout=self.timeout)
      r.raise_for_status()
    except requests.exceptions.RequestException:
      LOG.exception('Failed to communicate with Finna API')
      return None

    result_data = r.json()
    if not 'status' in result_data or result_data['status'] != 'OK':
      LOG.error('Finna query was not succesfull', extra={'data': {'result_data': repr(result_data)}})
      return None

    LOG.debug('Got result from Finna', extra={'data': {'result_data': repr(result_data)}})
    return result_data

  def search(self, search_term, facet_type=None, facet_value=None, page=1, limit=20, language='fi'):
    url = FinnaClient.API_ENDPOINT + 'search'
    payload = {
      'lookfor': search_term,
      'filter[]': ['format:'+self.material_type, 'building:'+self.organisation, 'online_boolean:"1"',],
      'page': page,
      'page': page,
      'limit': limit,
      'lng': language,
    }
    if facet_type and facet_value:
      payload['filter[]'].append(facet_type + ":" + facet_value)

    try:
      r = requests.get(url, params=payload, timeout=self.timeout)
      r.raise_for_status()
    except requests.exceptions.RequestException:
      LOG.error('Failed to communicate with Finna API', exc_info=True,
          extra={'data': {'status_code': r.status_code, 'response': repr(r.text)}})
      return None

    result_data = r.json()
    if not 'status' in result_data or result_data['status'] != 'OK':
      LOG.error('Finna query was not succesfull', extra={'data': {'result_data': repr(result_data)}})
      return None

    LOG.debug('Got result from Finna', extra={'data': {'result_data': repr(result_data)}})
    if limit > 0:
      pages = math.ceil(result_data['resultCount'] / float(limit))
    else:
      pages = 1
    result_data['pages'] = int(pages)
    result_data['limit'] = limit
    result_data['page'] = page
    return result_data

  def get_record(self, record_id):
    url = FinnaClient.API_ENDPOINT + 'record'
    payload = {
      'id': record_id,
      'field[]': ['id', 'authors','buildings', 'formats', 'genres', 'humanReadablePublicationDates',
        'imageRights', 'images', 'institutions', 'languages', 'originalLanguages', 'presenters',
        'publicationDates', 'rating', 'series', 'subjects', 'summary', 'title', 'year', 'rawData',],
    }
    try:
      r = requests.get(url, params=payload, timeout=self.timeout)
      r.raise_for_status()
    except requests.exceptions.RequestException:
      LOG.error('Failed to communicate with Finna API', exc_info=True,
          extra={'data': {'status_code': r.status_code, 'response': repr(r.text)}})
      return None

    result_data = r.json()
    if not 'status' in result_data or result_data['status'] != 'OK':
      LOG.error('Finna query was not succesfull', extra={'data': {'result_data': repr(result_data)}})
      return None

    LOG.debug('Got result from Finna', extra={'data': {'result_data': repr(result_data)}})
    return result_data


DEFAULT_CLIENT = FinnaClient()

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
