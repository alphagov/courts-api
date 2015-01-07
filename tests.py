import falcon
from uuid import uuid4 as random_uuid
from falcon.testing import TestBase
from json import dumps

from app.app import courts_api


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


class CourtRequestTests(CourtsAPITestBase):
    def test_putting_a_valid_court(self):
        self.put(VALID_REQUEST_BODY)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
