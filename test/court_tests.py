from jsonschema import ValidationError
import unittest

from courts_api.court import Court
from helpers import random_uuid, VALID_REQUEST_BODY


class CourtTestCase(unittest.TestCase):
    def test_instantiation_sets_attributes(self):
        uuid = random_uuid()
        court = Court(uuid, VALID_REQUEST_BODY)
        self.assertEqual(uuid, court.uuid)
        self.assertEqual('Barnsley Court', court.name)

    def test_court_is_validated_on_instantiation(self):
        with self.assertRaises(ValidationError) as context_manager:
            Court(random_uuid(), {'name': 'Barnsley Court'})
        self.assertEqual(
            "u'slug' is a required property",
            context_manager.exception.message
        )

    def test_base_path(self):
        court = Court(random_uuid(), VALID_REQUEST_BODY)
        self.assertEqual('/courts/barnsley-court', court.base_path)

    def test_public_url(self):
        court = Court(random_uuid(), VALID_REQUEST_BODY)
        self.assertEqual(
            'http://www.dev.gov.uk/courts/barnsley-court',
            court.public_url
        )

    def test_publishing_api_format(self):
        uuid = random_uuid()
        name = 'Barnsley Court'
        slug = 'barnsley-court'
        expected = {
            'base_path': '/courts/barnsley-court',
            'content_id': uuid,
            'title': name,
            'format': 'court',
            'update_type': 'major',
            'publishing_app': 'courts-api',
            'rendering_app': 'courts-frontend',
            'routes': [
                {'path': '/courts/barnsley-court', 'type': 'exact'}
            ]
        }
        self.assertEqual(
            expected,
            Court(uuid, {'name': name, 'slug': slug}).publishing_api_format
        )

    def test_response_format(self):
        name = 'Barnsley Court'
        slug = 'barnsley-court'
        expected = {
            'name': name,
            'public_url': 'http://www.dev.gov.uk/courts/barnsley-court'
        }
        self.assertEqual(
            expected,
            Court(random_uuid(), {'name': name, 'slug': slug}).response_format
        )
