import falcon
from mock import patch, Mock
from requests import ConnectionError
import unittest

from courts_api.publishing_api import PublishingAPI


class PublishingAPITestCase(unittest.TestCase):
    def test_url_for_data(self):
        data = {'base_path': '/courts/barnsley-court'}
        expected = 'http://publishing-api.dev.gov.uk/content/courts/barnsley-court'
        self.assertEqual(
            expected,
            PublishingAPI._url_for_data(data)
        )

    @patch('requests.put')
    def test_successful_put(self, put_mock):
        put_mock.return_value = Mock(status_code=201)
        data = {'base_path': '/courts/barnsley-court'}
        resp = PublishingAPI.put(data)
        self.assertEqual(201, resp.status_code)

    @patch('requests.put')
    def test_put_with_connection_error(self, put_mock):
        put_mock.side_effect = ConnectionError('Connection aborted.')
        data = {'base_path': '/courts/barnsley-court'}
        with self.assertRaises(falcon.HTTPServiceUnavailable):
            PublishingAPI.put(data)
        self.assertTrue(put_mock.called)
