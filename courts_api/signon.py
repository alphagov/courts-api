import requests
import settings
from courts_api.plek import url_for_application


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
    return response.status_code == 200
