import falcon
from json import loads
from mock import patch, Mock

from helpers import (CourtsAPITestBase, court_path, random_uuid,
    VALID_REQUEST_BODY, VALID_REQUEST_HEADERS)
from courts_api.errors import HTTP_422


@patch('courts_api.signon.authenticate_api_user', new=Mock(return_value=True))
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
