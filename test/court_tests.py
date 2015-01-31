import unittest

from courts_api.court import Court
from helpers import random_uuid


class CourtTestCase(unittest.TestCase):
    def test_instantiation_sets_attributes(self):
        uuid = random_uuid()
        court = Court(uuid, {'name': 'Barnsley Court'})
        self.assertEqual(uuid, court.uuid)
        self.assertEqual('Barnsley Court', court.name)

    def test_base_path(self):
        court = Court(random_uuid(), {'slug': 'barnsley-court'})
        self.assertEqual('/courts/barnsley-court', court.base_path)

    def test_public_url(self):
        court = Court(random_uuid(), {'slug': 'barnsley-court'})
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
