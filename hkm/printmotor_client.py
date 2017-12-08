import logging

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

LOG = logging.getLogger(__name__)


class PrintmotorClient(object):

    API_ENDPOINT = settings.HKM_PRINTMOTOR_API_ENDPOINT
    USERNAME = settings.HKM_PRINTMOTOR_USERNAME
    PASSWORD = settings.HKM_PRINTMOTOR_PASSWORD
    API_KEY = settings.HKM_PRINTMOTOR_API_KEY

    def post(self, order_collection):
        LOG.debug(PrintmotorClient.API_KEY)
        url = PrintmotorClient.API_ENDPOINT
        order = order_collection.product_orders.first()
        products = order_collection.product_orders.all()

        product_payload = []

        for product in products:
            for i in product.amount:
                product_payload.append({
                    'layoutName': product.product_name,
                    'amount': product.amount,
                    'customization': [
                        {
                            'fieldName': "image",
                            'value': product.crop_image_url,
                        }
                    ],
                    'endUserPrice': {
                        'priceValue': float(product.total_price),
                        'currencyIso4217': "EUR",
                    }
                })

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
            'products': product_payload,
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
        except requests.exceptions.RequestException as e:
            LOG.error(e, exc_info=True, extra={'data': {'order_hash': order_collection.pk}})
            return None


client = PrintmotorClient()
