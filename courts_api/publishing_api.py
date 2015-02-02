import falcon
import logging
import requests

from courts_api.plek import url_for_application

logger = logging.getLogger(__name__)


class PublishingAPI(object):
    @staticmethod
    def _url_for_data(data):
        """Returns the full Publishing API URL to PUT the given data to.

        eg https://publishing-api.preview.alphagov.co.uk/content/courts/barnsley-court
        """
        return '{0}/content{1}'.format(
            url_for_application('publishing-api').rstrip('/'),
            data['base_path'],
        )

    @classmethod
    def put(cls, data):
        """PUT data to the publishing-api and return the response.

        If the request raises an exception, or if the response status is 5xx,
        this method raises an instance of Falcon's 503 error class.
        """
        server_error = False
        try:
            publishing_api_response = requests.put(
                cls._url_for_data(data),
                json=data,
            )
            if 500 <= publishing_api_response.status_code <= 599:
                logger.warn(
                    '{} received from Publishing API'.format(publishing_api_response.status_code),
                    extra={'publishing_api_response_body': publishing_api_response.content}
                )
                server_error = True
        except requests.exceptions.RequestException as e:
            logger.warn(repr(e))
            server_error = True

        if server_error:
            raise falcon.HTTPServiceUnavailable(
                'Temporarily Unavailable',
                'Please try again later',
                30  # value for Retry-After header
            )

        return publishing_api_response
