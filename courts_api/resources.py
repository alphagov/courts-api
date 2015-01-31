import falcon
import json
import jsonschema

from courts_api.court import Court
from courts_api.errors import HTTP_422, HTTPUnprocessableEntity
from courts_api.hooks import (authenticate, check_client_is_sending_json,
    check_client_accepts_json)
from courts_api.plek import url_for_application
from courts_api.publishing_api import PublishingAPI


class HealthcheckResource(object):

    def on_get(self, req, resp):
        resp.body = 'OK'


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
        court = self._court_from_request(uuid, req)

        publishing_api_response = PublishingAPI.put(court.publishing_api_format)

        self._set_response_status(resp, publishing_api_response.status_code)
        self._set_response_body(resp, publishing_api_response, court)
        self._set_response_location_header(resp, publishing_api_response, uuid)

    @staticmethod
    def _parse_body(req):
        """Parse the request body and return it as a dict."""
        try:
            data = json.loads(req.context['body'])
        except ValueError:
            raise falcon.HTTPBadRequest(
                'Bad Request',
                'The request body could not be parsed as JSON.'
            )
        return data

    def _court_from_request(self, uuid, req):
        """Construct a Court instance from request data.

        Court validates the data against the JSON schema, so this handles the
        conversion of any errors raised there into error responses.
        """
        data = self._parse_body(req)
        try:
            return Court(uuid, data)
        except jsonschema.SchemaError:
            raise falcon.HTTPInternalServerError
        except jsonschema.ValidationError as e:
            raise HTTPUnprocessableEntity('Validation failed', e.message)

    @staticmethod
    def _set_response_status(resp, status_code):
        """Set resp.status based on the given status code."""
        if status_code == 422:
            resp.status = HTTP_422
        else:
            resp.status = getattr(falcon, 'HTTP_{}'.format(status_code))

    def _set_response_body(self, resp, publishing_api_response, court):
        """Set the response body.

        If the response from the publishing API was 4xx, include any returned
        errors in resp.body. If the court was successfully sent to the
        publishing API, include basic details about it instead.
        """
        publishing_api_resp_body = publishing_api_response.json()
        status_code = publishing_api_response.status_code

        if status_code in [200, 201]:
            resp.body = json.dumps(court.response_format)
        elif 400 <= status_code <= 499 and \
                'errors' in publishing_api_resp_body:
            resp.body = json.dumps({
                'errors': publishing_api_resp_body['errors']}
            )

    @staticmethod
    def _set_response_location_header(resp, publishing_api_response, uuid):
        """Set the location header if the court has just been created.

        This is the courts-api URL for the court which should be used for future
        requests to update it, not the public URL at which it has been published.
        """
        if publishing_api_response.status_code == 201:
            # This is the URL to use for future updates to this court (it's
            # the same as the one used for the current request):
            resp.location = '{0}/courts/{1}'.format(
                url_for_application('courts-api'),
                uuid,
            )
