import falcon

from resources import CourtsResource, CourtResource, HealthcheckResource


courts_api = application = falcon.API()

courts_api.add_route('/courts', CourtsResource())
courts_api.add_route('/courts/{uuid}', CourtResource())
courts_api.add_route('/healthcheck', HealthcheckResource())
