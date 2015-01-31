import falcon
import json

from courts_api.plek import url_for_application
from courts_api.publishing_api import PublishingAPI
from validators import (authenticate, check_client_is_sending_json,
    check_client_accepts_json, validate_court)


class HealthcheckResource(object):

    def on_get(self, req, resp):
        resp.body = 'OK'


@falcon.before(check_client_is_sending_json)
@falcon.before(check_client_accepts_json)
class CourtsResource(object):

    def on_get(self, req, resp):
        court = {'name': 'Barnsley Court', 'slug': 'barnsley-court'}
        resp.body = json.dumps({'courts': [court]})
        resp.status = falcon.HTTP_200


@falcon.before(authenticate)
@falcon.before(check_client_is_sending_json)
@falcon.before(check_client_accepts_json)
class CourtResource(object):

    def on_put(self, req, resp, uuid):
        data = json.loads(req.context['body'])
        validate_court(data)

        publishing_api_response = PublishingAPI.put(
            self._court_publishing_api_format(uuid, data)
        )

        if publishing_api_response.status_code in [200, 201]:
            resp.body = json.dumps({
                'status': 'created',
                'uuid': uuid,
                'name': data['name'],
                'slug': data['slug']
            })
            resp.status = getattr(falcon, 'HTTP_{}'.format(publishing_api_response.status_code))
            if publishing_api_response.status_code == 201:
                # This is the URL to use for future updates to this court (it's
                # the same as the one used for the current request):
                resp.location = '{0}/courts/{1}'.format(
                    url_for_application('courts-api'),
                    uuid,
                )
        else:
            raise falcon.HTTPServiceUnavailable(
                'Temporarily Unavailable',
                'Please try again later',
                30  # value for Retry-After header
            )

    @staticmethod
    def _base_path(court_body):
        return '/courts/{}'.format(court_body['slug'])

    def _court_publishing_api_format(self, court_id, court_body):
        return {
            'base_path': self._base_path(court_body),
            'content_id': court_id,
            'title': court_body['name'],
            'format': 'court',
            'update_type': 'major',
            'publishing_app': 'courts-api',
            'rendering_app': 'courts-frontend',
            'routes': [
                {'path': self._base_path(court_body), 'type': 'exact'}
            ]
        }