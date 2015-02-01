import logging
from logstash_formatter import LogstashFormatter
import os

from production_settings import *


def govuk_env():
    return os.getenv('GOVUK_ENV', 'development')

def app_domain():
    return os.getenv('GOVUK_APP_DOMAIN', 'dev.gov.uk')


# Logging setup:
file_handler = logging.FileHandler("log/%s.json.log" % govuk_env())

file_formatter = LogstashFormatter()
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)

errbit_handler = ErrbitHandler(
    errbit_url=AIRBRAKE_HOST,
    api_key=AIRBRAKE_API_KEY,
    environment=AIRBRAKE_ENVIRONMENT_NAME
)
errbit_handler.setLevel(logging.ERROR)

logger = logging.getLogger('courts_api')
logger.addHandler(file_handler)
logger.addHandler(errbit_handler)
logger.setLevel(logging.INFO)
