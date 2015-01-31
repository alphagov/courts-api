import falcon
import requests

from courts_api.plek import url_for_application


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
        """PUT data to the publishing-api."""
        print 'Sending to {}'.format(cls._url_for_data(data))
        try:
            publishing_api_response = requests.put(
                cls._url_for_data(data),
                data=data,
            )
        except requests.ConnectionError:
            raise falcon.HTTPServiceUnavailable(
                'Temporarily Unavailable',
                'Please try again later',
                30  # value for Retry-After header
            )

        return publishing_api_response
