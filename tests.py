import falcon
from uuid import uuid4 as random_uuid
from falcon.testing import TestBase
from json import dumps, loads

from app.app import courts_api
from app.courts import HTTP_422


def court_path(court_uuid):
    return '/courts/{}'.format(court_uuid)

VALID_REQUEST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

VALID_REQUEST_BODY = {
    'name': 'Barnsley Court',
    'slug': 'barnsley-court'
}


class CourtsAPITestBase(TestBase):
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
            body=dumps(VALID_REQUEST_BODY),
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
