import falcon
import json
from jsonschema import validate, ValidationError, SchemaError

from errors import HTTPUnprocessableEntity


with open('court_schema.json') as schema:
    COURT_SCHEMA = json.load(schema)


def validate_court(data):
    try:
        validate(data, COURT_SCHEMA)
    except SchemaError:
        raise falcon.HTTPInternalServerError
    except ValidationError as e:
        raise HTTPUnprocessableEntity('Validation failed', e.message)


def check_client_accepts_json(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable('You must accept JSON')


def check_client_is_sending_json(req, resp, params):
    if req.content_type != 'application/json':
        raise falcon.HTTPUnsupportedMediaType('You must send JSON')
