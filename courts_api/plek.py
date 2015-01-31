from urlparse import urlunsplit

import settings


def url_for_application(application):
    """Return the base URL for the given application."""
    scheme = 'https'
    if settings.govuk_env() == 'development':
        scheme = 'http'
    application_hostname = '{0}.{1}'.format(application, settings.app_domain())
    return urlunsplit((scheme, application_hostname, '', '', ''))
