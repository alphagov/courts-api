import logging
import StringIO


logger = logging.getLogger(__name__)


def request_log_field(environ):
    """Return a string representing the request for logging.

    Eg 'PUT /courts/12345?foo=bar HTTP/1.1'
    """
    relative_url = environ['PATH_INFO']
    query_string = environ['QUERY_STRING']
    if query_string:
        relative_url += '?{}'.format(query_string)

    return '{0} {1} {2}'.format(
        environ['REQUEST_METHOD'],
        relative_url,
        environ['SERVER_PROTOCOL']
    )


def extra_log_data(environ, request_body):
    """Return a dict of extra fields to log.

    'status' is empty because we want to log these fields even when the
    application throws an uncaught exception, which may happen before
    start_response has been called; even if start_response has been called, the
    status passed to it will not be the one returned to the client in this case.
    'status' must be filled in once the application has returned a response in
    order for it to be correctly logged.
    """
    return {
        'request': request_log_field(environ),
        'method': environ['REQUEST_METHOD'],
        'govuk_request_id': environ.get('HTTP_GOVUK_REQUEST_ID', ''),
        'request_body': request_body,
        'status': ''
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

        extra = extra_log_data(environ, request_body)
        try:
            response = self.application(environ, start_response_wrapper)
        except Exception as e:
            logger.error(repr(e), extra=extra)
            raise

        extra['status'] = start_response_wrapper.status_code
        logger.info('', extra=extra)
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

    @property
    def status_code(self):
        """Return the status code as a string."""
        return self.status.split()[0]
