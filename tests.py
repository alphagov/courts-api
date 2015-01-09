import falcon
from uuid import uuid4 as random_uuid
from falcon.testing import TestBase
from json import dumps, loads
from mock import patch

from app.app import application as courts_api
from app.errors import HTTP_422


def court_path(court_uuid):
    return '/courts/{}'.format(court_uuid)

VALID_REQUEST_HEADERS = {
    'Authorization': 'Bearer 1234567890',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

VALID_REQUEST_BODY = {
    'name': 'Barnsley Court',
    'slug': 'barnsley-court'
}


class CourtsAPITestBase(TestBase):
    "A test base for testing requests to the courts API"
    def setUp(self):
        super(CourtsAPITestBase, self).setUp()
        self.api = courts_api

    def put(self, body, headers={}, court_uuid=None):
        merged_headers = dict(VALID_REQUEST_HEADERS.items() + headers.items())
        if not court_uuid:
            court_uuid = random_uuid()
        return self.simulate_request(
            court_path(court_uuid),
            method='PUT',
            headers=merged_headers,
            body=dumps(body)
        )

    def assertStatus(self, status):
        "Compare the mock response status to a Falcon-style status code string"
        return self.assertEqual(self.srmock.status, status)


class HealthcheckTests(CourtsAPITestBase):
    def test_healthcheck(self):
        resp = self.simulate_request('/healthcheck', decode='utf-8')
        self.assertStatus(falcon.HTTP_200)
        self.assertEqual(resp, 'OK')


class CourtRequestTests(CourtsAPITestBase):
    def test_putting_a_valid_court(self):
        self.put(VALID_REQUEST_BODY)
        self.assertStatus(falcon.HTTP_201)

    def test_putting_an_invalid_court(self):
        self.put({'foo': 'bar'})
        self.assertStatus(HTTP_422)

    def test_putting_with_unsupported_media_type(self):
        self.put(VALID_REQUEST_BODY, headers={'Content-Type': 'text/plain'})
        self.assertStatus(falcon.HTTP_415)

    def test_putting_without_accepting_json(self):
        self.put(VALID_REQUEST_BODY, headers={'Accept': 'application/xml'})
        self.assertStatus(falcon.HTTP_406)

    def test_get_request_for_court_not_allowed(self):
        self.simulate_request(
            court_path(random_uuid()),
            method='GET',
            headers=VALID_REQUEST_HEADERS,
        )
        self.assertStatus(falcon.HTTP_405)

    def test_get_all_courts(self):
        resp = self.simulate_request(
            '/courts',
            method='GET',
            headers=VALID_REQUEST_HEADERS
        )
        self.assertStatus(falcon.HTTP_200)
        self.assertIn('courts', loads(resp[0]))


class AuthenticationTests(CourtsAPITestBase):
    def test_authentication_without_authorization_header(self):
        resp = self.put(VALID_REQUEST_BODY, headers={'Authorization': None})
        self.assertStatus(falcon.HTTP_401)
        self.assertEqual('Authentication Required', loads(resp[0])['title'])
        self.assertEqual('Bearer', self.srmock.headers_dict['www-authenticate'])

    def test_authentication_with_malformed_authorization_header(self):
        resp = self.put(VALID_REQUEST_BODY, headers={'Authorization': 'hi let me in please'})
        self.assertStatus(falcon.HTTP_401)
        self.assertEqual('Authentication Required', loads(resp[0])['title'])
        self.assertEqual('Bearer', self.srmock.headers_dict['www-authenticate'])

    def test_authentication_with_missing_bearer_token(self):
        resp = self.put(VALID_REQUEST_BODY, headers={'Authorization': 'Bearer'})
        self.assertStatus(falcon.HTTP_401)
        self.assertEqual('Authentication Required', loads(resp[0])['title'])
        self.assertEqual('Bearer', self.srmock.headers_dict['www-authenticate'])

    @patch('app.signon.authenticate_api_user')
    def test_authentication_with_invalid_bearer_token(self, signon_mock):
        signon_mock.return_value.status = 401
        resp = self.put(VALID_REQUEST_BODY)

        self.assertStatus(falcon.HTTP_401)
        self.assertEqual('Authentication Failed', loads(resp[0])['title'])
        self.assertEqual(
            'Bearer error="invalid_token"',
            self.srmock.headers_dict['www-authenticate']
        )
