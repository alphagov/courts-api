import falcon
import json

from falcon.http_error import HTTPError
from jsonschema import validate, ValidationError, SchemaError


class HTTPUnprocessableEntity(HTTPError):
    """422 Unprocessable Entity.

    The server understands the content type of the request entity, and the
    syntax of the request entity is correct, but was unable to process the
    contained instructions. (RFC 4918)
    Args:
        title (str): Error title (e.g., 'Required fields are missing').
        description (str): Human-friendly description of the error, along with
            a helpful suggestion or two.
        kwargs (optional): Same as for ``HTTPError``.
    """

    def __init__(self, title, description, **kwargs):
        HTTPError.__init__(self, '422 Unprocessable Entity', title, description, **kwargs)


def check_client_accepts_json(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable('You must accept JSON')


def validate_court(data):
    with open('court_schema.json') as schema:
        try:
            validate(data, json.load(schema))
        except SchemaError:
            raise falcon.HTTPInternalServerError
        except ValidationError as e:
            raise HTTPUnprocessableEntity('Validation failed', e.message)


@falcon.before(check_client_accepts_json)
class CourtsResource(object):

    def on_get(self, req, resp):
        court = {'name': 'Barnsley Court', 'slug': 'barnsley-court'}
        resp.body = json.dumps({'courts': [court]})
        resp.status = falcon.HTTP_200


@falcon.before(check_client_accepts_json)
class CourtResource(object):

    def on_put(self, req, resp, uuid):
        data = json.load(req.stream)
        validate_court(data)

        resp.body = json.dumps({
            'status': 'created',
            'uuid': uuid,
            'name': data['name'],
            'slug': data['slug']
        })
        resp.location = 'https://www.preview.alphagov.co.uk/courts/{}'.format(data['slug'])
        resp.status = falcon.HTTP_201
