import logging
import requests
import base64

from requests.auth import HTTPBasicAuth
from django.forms.models import model_to_dict

from hkm import settings

LOG = logging.getLogger(__name__)


class PrintmotorClient(object):

    API_ENDPOINT = settings.PRINTMOTOR_API_ENDPOINT
    USERNAME = settings.PRINTMOTOR_USERNAME
    PASSWORD = settings.PRINTMOTOR_PASSWORD
    API_KEY = settings.PRINTMOTOR_API_KEY

    def post(self, order):
        LOG.debug(PrintmotorClient.API_KEY)
        url = PrintmotorClient.API_ENDPOINT
        layout = order.product_name

        # order['phone'] = model_to_dict(order['phone'], ['national_number'])['national_number']

        payload = {
            'orderer': {
                'firstName': order.first_name,
                'lastName': order.last_name,
                'emailAddress': order.email,
                'phone': str(order.phone),
            },
            'address': {
                'address': order.street_address,
                'postalArea': order.city,
                'postalCode': order.postal_code,
                'countryIso2': "FI",
            },
            'products': [
                {
                    'layoutName': layout,
                    'amount': order.amount,
                    'customization': [
                        {
                            'fieldName': "image",
                            'value': order.crop_image_url,
                        }
                    ],
                    'endUserPrice': {
                        'priceValue': float(order.total_price),
                        'currencyIso4217': "EUR",
                    }
                }
            ],
            'meta': {
                "reference": order.order_hash,
            }
        }

        LOG.debug(payload)

        try:

            r = requests.post(url, json=payload, auth=HTTPBasicAuth(self.USERNAME, self.PASSWORD), headers={
                'X-Printmotor-Service': PrintmotorClient.API_KEY,
                'Content-Type': 'application/json',
            })
            LOG.debug(r.status_code)
            return r.status_code
        except requests.exceptions.RequestException:
            LOG.error('Failed to communicate with Printmotor API')
            return None


client = PrintmotorClient()
