import unittest

from courts_api.middleware import request_log_field


class LoggingMiddlewareHelperTests(unittest.TestCase):
    ENVIRON = {
        'REQUEST_METHOD': 'PUT',
        'PATH_INFO': '/courts/12345',
        'QUERY_STRING': '',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }

    def test_request_log_field_without_query_string(self):
        expected = 'PUT /courts/12345 HTTP/1.1'
        self.assertEqual(expected, request_log_field(self.ENVIRON))

    def test_request_log_field_with_query_string(self):
        environ = self.ENVIRON.copy()
        environ['QUERY_STRING'] = 'foo=bar'
        expected = 'PUT /courts/12345?foo=bar HTTP/1.1'
        self.assertEqual(expected, request_log_field(environ))
