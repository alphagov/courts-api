import unittest

from courts_api.publishing_api import PublishingAPI


class PublishingAPITestCase(unittest.TestCase):
    def test_url_for_data(self):
        data = {'base_path': '/courts/barnsley-court'}
        expected = 'http://publishing-api.dev.gov.uk/content/courts/barnsley-court'
        self.assertEqual(
            expected,
            PublishingAPI._url_for_data(data)
        )
