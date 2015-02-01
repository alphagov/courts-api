from json import dumps
import unittest

from courts_api.middleware import request_log_field, extra_log_data
from test.helpers import ENVIRON


class LoggingMiddlewareHelperTests(unittest.TestCase):
    def test_request_log_field_without_query_string(self):
        expected = 'PUT /courts/12345 HTTP/1.1'
        self.assertEqual(expected, request_log_field(ENVIRON))

    def test_request_log_field_with_query_string(self):
        environ = ENVIRON.copy()
        environ['QUERY_STRING'] = 'foo=bar'
        expected = 'PUT /courts/12345?foo=bar HTTP/1.1'
        self.assertEqual(expected, request_log_field(environ))

    def test_extra_log_data(self):
        request_body = dumps({'name': 'Barnsley Court'})
        expected = {
            'request': 'PUT /courts/12345 HTTP/1.1',
            'method': 'PUT',
            'govuk_request_id': '',
            'request_body': '{"name": "Barnsley Court"}',
            'status': 422
        }
        self.assertEqual(expected, extra_log_data(ENVIRON, request_body, 422))

    def test_extra_log_data_with_govuk_request_id(self):
        environ = ENVIRON.copy()
        environ['HTTP_GOVUK_REQUEST_ID'] = 'abcdefg'
        request_body = dumps({'name': 'Barnsley Court'})
        self.assertEqual(
            'abcdefg',
            extra_log_data(environ, request_body, 422)['govuk_request_id']
        )
