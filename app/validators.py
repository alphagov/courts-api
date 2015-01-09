import falcon
import json
from re import match
from jsonschema import validate, ValidationError, SchemaError

from errors import HTTPUnprocessableEntity
import signon


with open('court_schema.json') as schema:
    COURT_SCHEMA = json.load(schema)


def validate_court(data):
    "Validate a data dict against the court request JSON schema"
    try:
        validate(data, COURT_SCHEMA)
    except SchemaError:
        raise falcon.HTTPInternalServerError
    except ValidationError as e:
        raise HTTPUnprocessableEntity('Validation failed', e.message)


def authenticate(req, resp, params):
    title = 'Authentication Required'
    description = "Set the 'Authorization' header to 'Bearer <your_token>'"
    scheme = 'Bearer'

    if not req.auth:  # Authorization header isn't set
        raise falcon.HTTPUnauthorized(title, description, scheme=scheme)

    header_match = match('^Bearer (?P<token>[a-f\d]+)$', req.auth)
    if header_match is None:  # header is malformed, can't get a token from it
        raise falcon.HTTPUnauthorized(title, description, scheme=scheme)

    # Ask signon if the token is valid
    if not signon.authenticate_api_user(header_match.group('token')):
        title = 'Authentication Failed'
        description = 'The provided token is invalid'
        scheme = 'Bearer error="invalid_token"'
        raise falcon.HTTPUnauthorized(title, description, scheme=scheme)


def check_client_accepts_json(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable('You must accept JSON')


def check_client_is_sending_json(req, resp, params):
    if req.content_type != 'application/json':
        raise falcon.HTTPUnsupportedMediaType('You must send JSON')
