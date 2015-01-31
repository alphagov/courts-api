import falcon
from json import loads
from mock import patch, Mock
from requests import ConnectionError

from helpers import (CourtsAPITestBase, court_path, random_uuid,
    VALID_REQUEST_BODY, VALID_REQUEST_HEADERS)
from courts_api.errors import HTTP_422


@patch('courts_api.signon.authenticate_api_user', new=Mock(return_value=True))
@patch('requests.put')
@patch('courts_api.middleware.logger')
class CourtRequestTests(CourtsAPITestBase):
    def test_putting_a_valid_court(self, logger_mock, put_mock):
        put_mock.return_value = Mock(status_code=201)
        self.put(VALID_REQUEST_BODY)

        self.assertStatus(falcon.HTTP_201)
        self.assertTrue(put_mock.called)
        # Assert that the info method on the logger is called:
        self.assertTrue(logger_mock.info.called)

    def test_putting_an_invalid_court(self, logger_mock, put_mock):
        self.put({'foo': 'bar'})

        self.assertStatus(HTTP_422)
        self.assertFalse(put_mock.called)
        self.assertTrue(logger_mock.info.called)

    def test_putting_with_unsupported_media_type(self, logger_mock, put_mock):
        self.put(VALID_REQUEST_BODY, headers={'Content-Type': 'text/plain'})

        self.assertStatus(falcon.HTTP_415)
        self.assertFalse(put_mock.called)
        self.assertTrue(logger_mock.info.called)

    def test_putting_without_accepting_json(self, logger_mock, put_mock):
        self.put(VALID_REQUEST_BODY, headers={'Accept': 'application/xml'})

        self.assertStatus(falcon.HTTP_406)
        self.assertFalse(put_mock.called)
        self.assertTrue(logger_mock.info.called)

    def test_get_request_for_court_not_allowed(self, logger_mock, put_mock):
        self.simulate_request(
            court_path(random_uuid()),
            method='GET',
            headers=VALID_REQUEST_HEADERS,
        )

        self.assertStatus(falcon.HTTP_405)
        self.assertFalse(put_mock.called)
        self.assertTrue(logger_mock.info.called)

    def test_get_all_courts(self, logger_mock, put_mock):
        resp = self.simulate_request(
            '/courts',
            method='GET',
            headers=VALID_REQUEST_HEADERS
        )

        self.assertStatus(falcon.HTTP_200)
        self.assertIn('courts', loads(resp[0]))
        self.assertFalse(put_mock.called)
        self.assertTrue(logger_mock.info.called)

    def test_publishing_api_times_out(self, logger_mock, put_mock):
        put_mock.return_value = Mock(status_code=504)
        resp = self.put(VALID_REQUEST_BODY)

        self.assertStatus(falcon.HTTP_503)
        self.assertEqual('Temporarily Unavailable', loads(resp[0])['title'])
        self.assertTrue(put_mock.called)
        self.assertTrue(logger_mock.info.called)

    def test_publishing_api_connection_error(self, logger_mock, put_mock):
        put_mock.side_effect = ConnectionError('Connection aborted.')
        resp = self.put(VALID_REQUEST_BODY)

        self.assertStatus(falcon.HTTP_503)
        self.assertEqual('Temporarily Unavailable', loads(resp[0])['title'])
        self.assertTrue(put_mock.called)
        self.assertTrue(logger_mock.info.called)
