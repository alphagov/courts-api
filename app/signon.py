from collections import namedtuple


def authenticate_api_user(token):
    return namedtuple('SignonResponse', ['status'])(200)
