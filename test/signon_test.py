import unittest
from mock import patch, Mock

from courts_api.signon import authenticate_api_user


@patch('settings.SIGNON_CLIENT_ID', 'IMANAPI')
class SignonTests(unittest.TestCase):
    @patch('requests.get')
    def test_successful_authentication(self, get_mock):
        get_mock.return_value = Mock(status_code=200)
        self.assertEqual(authenticate_api_user('1234567890'), True)
        get_mock.assert_called_once_with(
            'http://signon.dev.gov.uk/user.json?client_id=IMANAPI',
            headers={'Authorization': 'Bearer 1234567890'}
        )

    @patch('requests.get')
    def test_unsuccessful_authentication(self, get_mock):
        get_mock.return_value = Mock(status_code=401)
        self.assertEqual(authenticate_api_user('notatoken'), False)
