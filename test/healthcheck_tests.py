import falcon

from helpers import CourtsAPITestBase


class HealthcheckTests(CourtsAPITestBase):
    def test_healthcheck(self):
        resp = self.simulate_request('/healthcheck', decode='utf-8')
        self.assertStatus(falcon.HTTP_200)
        self.assertEqual(resp, 'OK')
