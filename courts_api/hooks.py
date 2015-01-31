import falcon
from re import match

import signon


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
