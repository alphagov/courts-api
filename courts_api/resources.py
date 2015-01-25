import falcon
import json
import logging

from courts_api.plek import url_for_application
from validators import (authenticate, check_client_is_sending_json,
    check_client_accepts_json, validate_court)


logger = logging.getLogger(__name__)


def request_log_field(req):
    """Return a string representing the request for logging.

    Eg 'PUT /courts/12345?foo=bar HTTP/1.1'
    """
    return '{0} {1} {2}'.format(
        req.method,
        req.relative_uri,
        req.env['SERVER_PROTOCOL']
    )

def extra_log_data(req, resp, req_body):
    """Return a dict of extra fields to log.
    """
    return {
        'request': request_log_field(req),
        'method': req.method,
        'govuk_request_id': req.get_header('GOVUK-Request-Id'),
        'request_body': req_body,
        'status': resp.status, # FIXME make this just 201, not '201 Created'
    }


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
        req_body = req.stream.read()
        data = json.loads(req_body)
        validate_court(data)

        print 'Sending to {}'.format(url_for_application('publishing-api'))

        resp.body = json.dumps({
            'status': 'created',
            'uuid': uuid,
            'name': data['name'],
            'slug': data['slug']
        })
        resp.location = 'https://www.preview.alphagov.co.uk/courts/{}'.format(data['slug'])
        resp.status = falcon.HTTP_201

        logger.info('PUT a court', extra=extra_log_data(req, resp, req_body))
