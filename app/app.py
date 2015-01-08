import falcon

from resources import CourtsResource, CourtResource, HealthcheckResource


application = falcon.API()

application.add_route('/courts', CourtsResource())
application.add_route('/courts/{uuid}', CourtResource())
application.add_route('/healthcheck', HealthcheckResource())
