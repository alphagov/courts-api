import falcon
import uuid
from falcon.testing import TestBase
from json import dumps

from app.app import api as courts_api


class CourtsAPITestBase(TestBase):
    def setUp(self):
        super(CourtsAPITestBase, self).setUp()
        self.api = courts_api


class CourtRequestTests(CourtsAPITestBase):
    def test_putting_a_valid_court(self):
        court_uuid = uuid.uuid4()
        request_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        request_body = {
            'name': 'Barnsley Court',
            'slug': 'barnsley-court'
        }
        self.simulate_request(
            '/courts/{}'.format(court_uuid),
            method='PUT',
            headers=request_headers,
            body=dumps(request_body)
        )

        self.assertEqual(self.srmock.status, falcon.HTTP_201)
