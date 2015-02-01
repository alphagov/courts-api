import logging
import StringIO


logger = logging.getLogger(__name__)


def request_log_field(environ):
    """Return a string representing the request for logging.

    Eg 'PUT /courts/12345?foo=bar HTTP/1.1'
    """
    return '{0} {1} {2}'.format(
        environ['REQUEST_METHOD'],
        environ['PATH_INFO'] + '?' + environ['QUERY_STRING'],
        environ['SERVER_PROTOCOL']
    )


def extra_log_data(environ, request_body, status_code):
    """Return a dict of extra fields to log."""
    return {
        'request': request_log_field(environ),
        'method': environ['REQUEST_METHOD'],
        'govuk_request_id': environ.get('HTTP_GOVUK-Request-Id', ''),
        'request_body': request_body,
        'status': status_code,
    }


class ResponseLoggerMiddleware(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        # Read the request body and replace it in the environ so that it can
        # be read later by the application:
        request_body = environ['wsgi.input'].read()
        environ['wsgi.input'] = StringIO.StringIO(request_body)

        start_response_wrapper = StartResponseWrapper(start_response)

        response = self.application(environ, start_response_wrapper)

        logger.info(
            '',
            extra=extra_log_data(
                environ,
                request_body,
                start_response_wrapper.status.split()[0]
            )
        )
        return response


class StartResponseWrapper(object):
    """A wrapper for start_response to record the status of the response."""

    def __init__(self, real_start_response):
        self.real_start_response = real_start_response

    def __call__(self, status, response_headers, exc_info=None):
        """Record the status string and then call the real start_response.

        status is eg '404 Not Found', not just the status code.
        """
        self.status = status
        return self.real_start_response(status, response_headers, exc_info)
