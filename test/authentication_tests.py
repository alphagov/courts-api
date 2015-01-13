import falcon
from json import loads
from mock import patch, Mock

from helpers import CourtsAPITestBase, VALID_REQUEST_BODY


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

    @patch('courts_api.signon.authenticate_api_user')
    def test_authentication_with_invalid_bearer_token(self, signon_mock):
        signon_mock.return_value = False
        resp = self.put(VALID_REQUEST_BODY)

        self.assertStatus(falcon.HTTP_401)
        self.assertEqual('Authentication Failed', loads(resp[0])['title'])
        self.assertEqual(
            'Bearer error="invalid_token"',
            self.srmock.headers_dict['www-authenticate']
        )

    @patch('requests.get')
    def test_authentication_when_signon_unavailable(self, get_mock):
        get_mock.return_value = Mock(status_code=504)  # Gateway Timeout
        resp = self.put(VALID_REQUEST_BODY)

        self.assertStatus(falcon.HTTP_503)
        self.assertEqual('Temporarily Unavailable', loads(resp[0])['title'])
        self.assertEqual('30', self.srmock.headers_dict['retry-after'])
