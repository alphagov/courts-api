import falcon
from resources import CourtsResource, CourtResource, HealthcheckResource
# Make sure that the logging config is executed early on:
from settings import logger


application = falcon.API()

application.add_route('/courts', CourtsResource())
application.add_route('/courts/{uuid}', CourtResource())
application.add_route('/healthcheck', HealthcheckResource())
