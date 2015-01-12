import unittest
from mock import patch, Mock

from courts_api.plek import url_for_application


class PlekTests(unittest.TestCase):
    def test_scheme_is_http_in_development(self):
        self.assertEqual(url_for_application('app'), 'http://app.dev.gov.uk')

    @patch('settings.govuk_env', new=Mock(return_value='production'))
    def test_scheme_is_https_in_production(self):
        self.assertEqual(url_for_application('app'), 'https://app.dev.gov.uk')

    @patch('settings.govuk_env', new=Mock(return_value='production'))
    @patch('settings.app_domain', new=Mock(return_value='preview.alphagov.co.uk'))
    def test_hostname_uses_app_domain(self):
        self.assertEqual(url_for_application('app'), 'https://app.preview.alphagov.co.uk')
