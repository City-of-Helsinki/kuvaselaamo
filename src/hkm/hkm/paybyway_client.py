
# -*- coding: utf-8 -*-

import logging
import requests
import hmac
import hashlib
import base64

from hkm import settings

LOG = logging.getLogger(__name__)


class PaybywayClient(object):

	API_ENDPOINT = 'https://dev.paybyway.com/pbwapi/auth_payment'
	API_KEY = settings.PBW_API_KEY
	SECRET_KEY = settings.PBW_SECRET_KEY
	# change dev to www when final -- this is a testing api
	timeout = 10

	def post(self, order_id, amount):
		url = PaybywayClient.API_ENDPOINT
		order_number = '%d' % order_id
		msg = '%s|%s' % (PaybywayClient.API_KEY, order_number)
		authcode = hmac.new(PaybywayClient.SECRET_KEY, msg, hashlib.sha256).hexdigest().upper()
		return_url = 'http://127.0.0.1:3333/order/%d/confirmation/' % order_id

		payload = {
			'version': 'w3.1',
			'api_key': PaybywayClient.API_KEY,
			'order_number': order_number,
			'amount': amount, #THIS SHOULD BE PRICE IN **CENTS**!! for testing reasons I am sending the no. of units ordered
			'currency': 'EUR',
			'payment_method': {
				'type': 'e-payment',
				'return_url': return_url,
				'notify_url': 'https://bar.test.com',
			},
			'authcode': authcode
		}

		try: 
			r = requests.post(url, json=payload)
			data = r.json()
			return data
		except requests.exceptions.RequestException:
			LOG.error('Failed to communicate with Paybyway API')
			return None


# just for testing this with a random order ID
client = PaybywayClient()
#client.post(139,777)

# /confirmation/?AUTHCODE=1CFDD5E0562B7772AF875859B009B05AF03670BE522097B20DC39E5B5229857A&RETURN_CODE=0&ORDER_NUMBER=hkmorder58&SETTLED=1
