from settings import app_domain


def url():
    return 'https://publishing-api.{}'.format(app_domain())
