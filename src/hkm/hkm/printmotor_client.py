import logging
import requests
import base64

from hkm import settings

LOG = logging.getLogger(__name__)


class PrintmotorClient(object):

  API_ENDPOINT = 'https://api.printmotor.io/api/v1/order'
  USERNAME = settings.PRINTMOTOR_USERNAME
  PASSWORD = settings.PRINTMOTOR_PASSWORD

  def post(self, order):
    url = PrintmotorClient.API_ENDPOINT

    payload = {
      'orderer': {
        'firstName' : order.first_name,
        'lastName' : order.last_name,
        'emailAddress' : order.email,
        'phone' : order.phone,
      },
      'address': {
        'address' : order.street_address,
        'address2' : "",
        'postalArea' : order.city,
        'postalCode' : order.postal_code,
        'countryIso2' : "FI",
      },
      'products': [ 
          {
            'layoutName' : "api-poster-a4",
            'amount' : order.amount,
                'customization' : [ 
                {
                  'fieldName' : "image",
                  'value' : order.crop_image_url,
                } 
            ],
            'endUserPrice' : {
              'priceValue' : order.total_price,
              'currencyIso4217' : "EUR"
            }
          } 
      ],
      'meta': {
        "reference": order.order_hash,
      }
    }

    try: 

      cred_string = '%s:%s' % (self.USERNAME, self.PASSWORD)
      auth = base64.b64encode(cred_string)
      headers = {
        'X-Printmotor-Service': '6ad12412f163584fc6627a854998babf',
        'Authorization': auth,
        'Content-Type': 'application/json',
      }

      r = requests.post(url, json=payload, headers=headers)
      data = r.json()
      return data
    except requests.exceptions.RequestException:
      LOG.error('Failed to communicate with Printmotor API')
      return None

client = PrintmotorClient()