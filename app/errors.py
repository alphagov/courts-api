from falcon.http_error import HTTPError


# 422 isn't in falcon.status_codes:
HTTP_422 = '422 Unprocessable Entity'


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
        HTTPError.__init__(self, HTTP_422, title, description, **kwargs)
