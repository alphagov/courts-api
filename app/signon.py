from collections import namedtuple


signon_response = namedtuple('SignonResponse', ['status'])

def authenticate_api_user(token):
    return signon_response(200)
