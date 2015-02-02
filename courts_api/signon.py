import falcon
import logging
import requests
import settings
from courts_api.plek import url_for_application

logger = logging.getLogger(__name__)


def authenticate_api_user(token):
    """Authenticate an API token against Signon.

    Return True if it is valid, and False otherwise.
    """
    url = '{0}/user.json?client_id={1}'.format(
        url_for_application('signon'),
        settings.SIGNON_CLIENT_ID
    )
    auth_header = 'Bearer {}'.format(token)
    response = requests.get(
        url,
        headers={'Authorization': auth_header}
    )
    if 500 <= response.status_code <= 599:
        logger.warn(
            '{} received from Signon'.format(response.status_code),
            extra={'signon_response_body': response.content}
        )
        raise falcon.HTTPServiceUnavailable(
            'Temporarily Unavailable',
            'Please try again later',
            30  # value for Retry-After header
        )
    return response.status_code == 200
