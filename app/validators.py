import falcon
import json
from jsonschema import validate, ValidationError, SchemaError

from errors import HTTPUnprocessableEntity


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
    if not req.auth:  # Authorization header isn't set
        title = 'Authentication Required'
        description = "Set the 'Authorization' header to 'Bearer <your_token>'"
        scheme = 'Bearer'
        raise falcon.HTTPUnauthorized(title, description, scheme=scheme)


def check_client_accepts_json(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable('You must accept JSON')


def check_client_is_sending_json(req, resp, params):
    if req.content_type != 'application/json':
        raise falcon.HTTPUnsupportedMediaType('You must send JSON')
