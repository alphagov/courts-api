import os


def app_domain():
    return os.getenv('GOVUK_APP_DOMAIN', 'dev.gov.uk')
