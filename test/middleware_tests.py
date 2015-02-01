from json import dumps
from mock import Mock, patch
import StringIO
import unittest

from courts_api.middleware import (request_log_field, extra_log_data,
    ResponseLoggerMiddleware)
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
            'status': ''
        }
        self.assertEqual(expected, extra_log_data(ENVIRON, request_body))

    def test_extra_log_data_with_govuk_request_id(self):
        environ = ENVIRON.copy()
        environ['HTTP_GOVUK_REQUEST_ID'] = 'abcdefg'
        request_body = dumps({'name': 'Barnsley Court'})
        self.assertEqual(
            'abcdefg',
            extra_log_data(environ, request_body)['govuk_request_id']
        )


class ResponseLoggerMiddlewareTests(unittest.TestCase):
    @staticmethod
    def call_application_via_middleware(application):
        application = ResponseLoggerMiddleware(application)

        environ = ENVIRON.copy()
        environ['wsgi.input'] = StringIO.StringIO('body text')
        start_response_mock = Mock(return_value=None)
        application(environ, start_response_mock)

    @patch('courts_api.middleware.logger')
    def test_logger_info_method_is_called_correctly(self, logger_mock):
        def fake_application(environ, start_response):
                start_response('200 OK', [])
                return ['response body']

        self.call_application_via_middleware(fake_application)

        logger_mock.info.assert_called_once_with(
            '',
            extra={
                'request': 'PUT /courts/12345 HTTP/1.1',
                'method': 'PUT',
                'govuk_request_id': '',
                'request_body': 'body text',
                'status': '200',
            }
        )

    @patch('courts_api.middleware.logger')
    def test_request_is_logged_with_uncaught_exception(self, logger_mock):
        class ApplicationException(Exception):
            pass

        def fake_application(environ, start_response):
            raise ApplicationException('oh noes')

        with self.assertRaises(ApplicationException):
            self.call_application_via_middleware(fake_application)

        logger_mock.error.assert_called_once_with(
            "ApplicationException('oh noes',)",
            extra={
                'request': 'PUT /courts/12345 HTTP/1.1',
                'method': 'PUT',
                'govuk_request_id': '',
                'request_body': 'body text',
                'status': ''
            }
        )
