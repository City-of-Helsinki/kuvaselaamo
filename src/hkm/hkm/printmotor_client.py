import logging
import requests
import base64

from requests.auth import HTTPBasicAuth
from django.forms.models import model_to_dict

from hkm import settings

LOG = logging.getLogger(__name__)


class PrintmotorClient(object):

  API_ENDPOINT = 'https://test.printmotor.io/api/v1/order'
  USERNAME = settings.PRINTMOTOR_USERNAME
  PASSWORD = settings.PRINTMOTOR_PASSWORD
  API_KEY = settings.PRINTMOTOR_API_KEY


  productNames = {
    '40 x 30 cm': 'api-poster-40x30'
  }

  def post(self, orderObject):
    LOG.debug(PrintmotorClient.API_KEY)
    url = PrintmotorClient.API_ENDPOINT
    if PrintmotorClient.productNames[orderObject.product_name]:
      layout = PrintmotorClient.productNames[orderObject.product_name]
    else:
      layout = 'unknown'

    order = model_to_dict(orderObject)
    # order['phone'] = model_to_dict(order['phone'], ['national_number'])['national_number']

    payload = {
      'orderer': {
        'firstName' : order['first_name'],
        'lastName' : order['last_name'],
        'emailAddress' : order['email'],
        'phone' : '0404040400',
      },
      'address': {
        'address' : order['street_address'],
        'postalArea' : order['city'],
        'postalCode' : order['postal_code'],
        'countryIso2' : "FI",
      },
      'products': [ 
          {
            'layoutName' : layout,
            'amount' : order['amount'],
                'customization' : [ 
                {
                  'fieldName' : "image",
                  'value' : order['image_url'], 
                } 
            ],
            'endUserPrice' : { 
              'priceValue' : int(order['total_price']),
              'currencyIso4217' : "EUR"
            }
          } 
      ],
      'meta': {
        "reference": order['order_hash'],
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