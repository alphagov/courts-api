import falcon
from json import loads, dumps
from mock import patch, Mock

from helpers import (CourtsAPITestBase, court_path, random_uuid,
    VALID_REQUEST_BODY, VALID_REQUEST_HEADERS)
from courts_api.errors import HTTP_422


@patch('courts_api.signon.authenticate_api_user', new=Mock(return_value=True))
@patch('requests.put')
@patch('courts_api.middleware.logger')
class CourtRequestTests(CourtsAPITestBase):
    def test_putting_a_valid_court(self, logger_mock, put_mock):
        put_mock.return_value = Mock(status_code=201)
        # We need to make an assertion later involving the uuid, so set it
        # explictly here:
        uuid = random_uuid()
        resp = self.put(VALID_REQUEST_BODY, court_uuid=uuid)

        self.assertStatus(falcon.HTTP_201)
        self.assertTrue(put_mock.called)
        # Assert that the info method on the logger is called:
        self.assertTrue(logger_mock.info.called)

        response_body = loads(resp[0])
        self.assertEqual('Barnsley Court', response_body['name'])
        self.assertEqual(
            'http://www.dev.gov.uk/courts/barnsley-court',
            response_body['public_url']
        )
        self.assertEqual(
            'http://courts-api.dev.gov.uk/courts/{}'.format(uuid),
            self.srmock.headers_dict['Location']
        )

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

    def test_putting_with_422_from_publishing_api(self, logger_mock, put_mock):
        """We expected this to succeed, but content-store validation failed"""
        put_mock.return_value = Mock(
            status_code=422,
            content=dumps({'errors': {'routes': ['are invalid']}})
        )
        resp = self.put(VALID_REQUEST_BODY)

        self.assertStatus(HTTP_422)
        self.assertTrue(put_mock.called)
        self.assertTrue(logger_mock.info.called)

        response_body = loads(resp[0])
        self.assertEqual(['are invalid'], response_body['errors']['routes'])

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
