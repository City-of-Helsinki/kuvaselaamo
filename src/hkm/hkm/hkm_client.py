
# -*- coding: utf-8 -*-

import logging
import urlparse
import urllib
import requests

LOG = logging.getLogger(__name__)


class HKMClient(object):
  timeout = 3

  def get_full_res_image_url(self, preview_image_url):
    """
    HKM image server responds with 200 text body response if there is no full res version for the
    image. This checks the response headers to find out whether full res image exists or not and
    returns the full res image url if it does. Else returns None
    """
    url_components = urlparse.urlparse(preview_image_url)
    qs_params = dict(urlparse.parse_qsl(url_components.query))
    qs_params['dataType'] = 'org'

    url_components = list(url_components)
    url_components[4] = urllib.urlencode(qs_params)
    url = urlparse.urlunparse(url_components)
    try:
      r = requests.head(url, timeout=self.timeout)
      r.raise_for_status()
    except requests.exceptions.RequestException:
      LOG.exception('Failed to communicate with HKM image server')
      return None

    LOG.debug('Got result from HKM image server',
        extra={'data': {'url': url, 'result_headers': repr(r.headers)}})
    try:
      content_type = r.headers['content-type']
      if 'image' in content_type:
        return url
    except KeyError:
      pass

    return None


DEFAULT_CLIENT = HKMClient()


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
