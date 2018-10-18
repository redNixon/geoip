import json
import unittest

from unittest import mock

from geoip.app import create_app
from tests.integration.helper import BaseTestCase


class TestIPEndpoint(BaseTestCase):
    """Test API endpoints functionality."""

    def test_localhost(self):
        """A 200 call with info on localhost at root."""
        expected = {'ip': '127.0.0.1', 'bogon': True}
        request, response = self.app.test_client.get('/')
        self.assertEqual(response.status, 200)
        self.assertEqual(
            response.json,
            expected,
        )

    def test_get_ip(self):
        """A profile for a specific IP should be shown on request."""
        expected = '8.8.8.8'
        request, response = self.app.test_client.get(f'/{expected}')
        self.assertEqual(response.status, 200)
        self.assertEqual(
            response.json.get('ip'),
            expected
        )

    def test_get_not_an_ip(self):
        """A malformed IP will be a bad request."""
        expected = {'error': 'Bad request', 'message': 'foo is not a valid ip'}
        request, response = self.app.test_client.get('/foo')
        self.assertEqual(
            response.json,
            expected,
        )
        self.assertEqual(response.status, 400)

    def test_bulk_malformed(self):
        """A malformed POST will result in a 400."""
        expected = {
            'error': 'Bad request',
            'message': 'This endpoint only supports a list.'
        }
        request, response = self.app.test_client.post(
            '/bulk', json={'bad': 'stuff'})
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json, expected)

    def test_bulk_with_malformed_ip(self):
        """A malformed IP in the POST will return a 400 error."""
        expected = {'error': 'Bad request', 'message': 'foo is not a valid ip'}
        request, response = self.app.test_client.post(
            '/bulk',
            json=['8.8.8.8', 'foo'],
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json, expected)

    def test_bulk_with_valid_ip(self):
        """Well formed IPs can be bulk submitted."""
        expected = {'results': [{'city': None,
                                 'continent': 'North America',
                                 'country': 'United States',
                                 'ip': '8.8.8.8',
                                 'locatio': {'lat': 37.751, 'lon': -97.822},
                                 'org': '15169 Google LLC'},
                                {'bogon': True, 'ip': '127.0.0.1'}]}

        request, response = self.app.test_client.post(
            '/bulk',
            json=['8.8.8.8', '127.0.0.1'],
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, expected)
