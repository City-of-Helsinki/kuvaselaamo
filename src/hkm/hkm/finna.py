
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

  def search(self, search_term, page=1, limit=20, language='fi'):
    url = FinnaClient.API_ENDPOINT + 'search'
    payload = {
      'lookfor': search_term,
      'filter[]': ['format:'+self.material_type, 'building:'+self.organisation, 'online_boolean:"1"'],
      'page': page,
      'limit': limit,
      'lng': language,
      'facet[]': ['author_facet', 'main_date_str', 'genre_facet', 'category_str_mv']
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

    if 'records' not in result_data:
      LOG.warning('No records with search term', extra={'data': {'url': repr(r.url)}})
      return None

    LOG.debug('Got result from Finna', extra={'data': {'result_data': repr(result_data)}})
    pages = math.ceil(result_data['resultCount'] / float(limit))
    result_data['pages'] = int(pages)
    result_data['limit'] = limit
    result_data['page'] = page
    return result_data


DEFAULT_CLIENT = FinnaClient()

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
