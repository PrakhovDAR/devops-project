import os
import requests
import sys
import time
import unittest

from common_logging import log

APP_URL = os.getenv('APP_URL', 'http://app:5000')


def wait_for_app() -> requests.Response | None:
	deadline = time.time() + 30
	while time.time() < deadline:
		try:
			resp = requests.get(APP_URL, timeout=3)
			if resp.status_code < 500:
				return resp
			log(f'App returned {resp.status_code}, retrying...')
		except requests.RequestException as e:
			log(f'Waiting for app: {e}', stream=sys.stderr, stream_name='stderr')
		time.sleep(2)
	return None


class TestHeaders(unittest.TestCase):
	def test_headers(self):
		log('Starting integration header checks')
		response = wait_for_app()
		if response is None:
			log('Application did not become ready', stream=sys.stderr, stream_name='stderr')
			self.fail('Application did not become ready')

		content_type = response.headers.get('Content-Type', '')
		if 'text/html' not in content_type:
			log(f'Unexpected Content-Type: {content_type}', stream=sys.stderr, stream_name='stderr')
			self.fail(f'Unexpected Content-Type: {content_type}')

		app_header = response.headers.get('X-Application-Name')
		if app_header != 'moevm-demo-app':
			log(f'Unexpected X-Application-Name: {app_header}', stream=sys.stderr, stream_name='stderr')
			self.fail(f'Unexpected X-Application-Name: {app_header}')

		debug_header = response.headers.get('X-Debug-Mode')
		if debug_header not in ('0', '1'):
			log(f'Unexpected X-Debug-Mode: {debug_header}', stream=sys.stderr, stream_name='stderr')
			self.fail(f'Unexpected X-Debug-Mode: {debug_header}')

		log('All header checks passed')


if __name__ == '__main__':
	unittest.main()