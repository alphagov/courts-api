import logging
from logstash_formatter import LogstashFormatter
import os

from production_settings import *


def govuk_env():
    return os.getenv('GOVUK_ENV', 'development')

def app_domain():
    return os.getenv('GOVUK_APP_DOMAIN', 'dev.gov.uk')


# Logging setup:
handler = logging.FileHandler("log/%s.json.log" % govuk_env())

formatter = LogstashFormatter()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger = logging.getLogger('courts_api')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
