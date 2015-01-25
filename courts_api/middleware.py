import logging


logger = logging.getLogger(__name__)


def request_log_field(req):
    """Return a string representing the request for logging.

    Eg 'PUT /courts/12345?foo=bar HTTP/1.1'
    """
    return '{0} {1} {2}'.format(
        req.method,
        req.relative_uri,
        req.env['SERVER_PROTOCOL']
    )


def extra_log_data(req, resp):
    """Return a dict of extra fields to log."""
    return {
        'request': request_log_field(req),
        'method': req.method,
        'govuk_request_id': req.get_header('GOVUK-Request-Id'),
        'request_body': req.context['body'],
        # FIXME falcon's handling of HTTPError subclasses isn't being logged -
        #     whenever our code raises one of them, the status is still logged
        #     as 200
        # FIXME make this just 201, not '201 Created'
        'status': resp.status,
    }


class ResponseLoggerMiddleware(object):
    def process_request(self, req, resp):
        # Read the body once and set it in the request context so that it is
        # available later on when we want to log it:
        req.context['body'] = req.stream.read()

    def process_response(self, req, resp):
        logger.info('', extra=extra_log_data(req, resp))
