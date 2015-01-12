from falcon.testing import TestBase
from json import dumps
from uuid import uuid4 as random_uuid

from courts_api.app import application as courts_api_application


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
        self.api = courts_api_application

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
