import falcon
from mock import patch

from helpers import CourtsAPITestBase


@patch('courts_api.middleware.logger')
class HealthcheckTests(CourtsAPITestBase):
    def test_healthcheck(self, logger_mock):
        resp = self.simulate_request('/healthcheck', decode='utf-8')
        self.assertStatus(falcon.HTTP_200)
        self.assertEqual(resp, 'OK')
        self.assertTrue(logger_mock.info.called)
