import falcon

from courts_api.middleware import ResponseLoggerMiddleware
from courts_api.resources import CourtsResource, CourtResource, HealthcheckResource
# Make sure that the logging config is executed early on:
from settings import logger


falcon_app = falcon.API()
falcon_app.add_route('/courts', CourtsResource())
falcon_app.add_route('/courts/{uuid}', CourtResource())
falcon_app.add_route('/healthcheck', HealthcheckResource())

application = ResponseLoggerMiddleware(falcon_app)
