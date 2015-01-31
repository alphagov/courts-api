import json
import jsonschema

from courts_api.plek import url_for_application


class Court(object):
    with open('court_schema.json') as schema:
        COURT_SCHEMA = json.load(schema)

    def __init__(self, uuid, data):
        self.validate(data)
        for key, value in data.items():
            setattr(self, key, value)
        self.uuid = uuid

    def validate(self, data):
        """Validate a data dict against the court request JSON schema."""
        jsonschema.validate(data, self.COURT_SCHEMA)

    @property
    def base_path(self):
        """The path at which the court will be published.

        This is required by the Publishing API.
        """
        return '/courts/{}'.format(self.slug)

    @property
    def public_url(self):
        """The full URL at which the court will be published."""
        return url_for_application('www') + self.base_path

    @property
    def publishing_api_format(self):
        """A dict representing the court as required by the Publishing API."""
        return {
            'base_path': self.base_path,
            'content_id': self.uuid,
            'title': self.name,
            'format': 'court',
            'update_type': 'major',
            'publishing_app': 'courts-api',
            'rendering_app': 'courts-frontend',
            'routes': [
                {'path': self.base_path, 'type': 'exact'}
            ]
        }

    @property
    def response_format(self):
        """A dict representing the court to be returned to the client."""
        return {
            'name': self.name,
            'public_url': self.public_url,
        }
