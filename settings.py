import os

from production_settings import *


def govuk_env():
    return os.getenv('GOVUK_ENV', 'development')

def app_domain():
    return os.getenv('GOVUK_APP_DOMAIN', 'dev.gov.uk')
