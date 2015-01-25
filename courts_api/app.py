import falcon
import logging
from logstash_formatter import LogstashFormatter

from resources import CourtsResource, CourtResource, HealthcheckResource
from settings import govuk_env


handler = logging.FileHandler("log/%s.json.log" % govuk_env())

formatter = LogstashFormatter()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger = logging.getLogger('courts_api')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

application = falcon.API()

application.add_route('/courts', CourtsResource())
application.add_route('/courts/{uuid}', CourtResource())
application.add_route('/healthcheck', HealthcheckResource())
