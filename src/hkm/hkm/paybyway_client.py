
# -*- coding: utf-8 -*-

import logging
import requests

LOG = logging.getLogger(__name__)


class PaybywayClient(object):

	API_ENDPOINT = 'https://dev.paybyway.com/pbwapi/auth_payment'
	API_KEY = '3632bfe8c82e99866e151e714d00c1e8ad49'
	# change dev to www when final -- this is a testing api
	timeout = 10

	def post(self, order_id, amount):
		url = PaybywayClient.API_ENDPOINT
		order_number = 'hkmorder%d' % order_id
		authcode = ''

		payload = {
			'version': 'w3.1',
			'api_key': PaybywayClient.API_KEY,
			'order_number': order_number,
			'amount': amount,
			'currency': 'EUR',
			'payment_method': {
				'type': 'e-payment',
				'return_url': 'https://foo.test.com',
				'notify_url': 'https://bar.test.com',
			},
			'authcode': authcode,
		}

		try: 
			r = requests.post(url, json=payload)
			result = r.json().get('result');
			print result				
		except requests.exceptions.RequestException:
			LOG.error('Failed to communicate with Paybyway API')
			return None


client = PaybywayClient()
client.post(666,777)
