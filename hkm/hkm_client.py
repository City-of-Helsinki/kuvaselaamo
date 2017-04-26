# -*- coding: utf-8 -*-

import logging
import urllib
import urlparse
from StringIO import StringIO

import requests
from PIL import Image

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
        except requests.exceptions.RequestException:
            LOG.error('Failed to communicate with HKM image server',
                      exc_info=True)
            return None
        else:
            try:
                r.raise_for_status()
                # raise requests.exceptions.HTTPError()
            except requests.exceptions.HTTPError:
                LOG.error('Failed to communicate with HKM image server', exc_info=True,
                          extra={'data': {'status_code': r.status_code, 'response': repr(r.text)}})
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

    def download_image(self, full_res_url):
        r = requests.get(full_res_url, stream=True)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException:
            LOG.error('Could not download a full res url',
                      extra={'data': {'img_url': full_res_url}})
        else:
            return Image.open(StringIO(r.content))
        return None


DEFAULT_CLIENT = HKMClient()


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
