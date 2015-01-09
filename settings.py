import os

from production_settings import *


def app_domain():
    return os.getenv('GOVUK_APP_DOMAIN', 'dev.gov.uk')

def signon_url():
    return 'http://signon.{}'.format(app_domain())
