import falcon
import json


def check_client_accepts_json(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable('You must accept JSON')


@falcon.before(check_client_accepts_json)
class CourtsResource(object):

    def on_get(self, req, resp):
        court = {'name': 'Barnsley Court', 'slug': 'barnsley-court'}
        resp.body = json.dumps({'courts': [court]})
        resp.status = falcon.HTTP_200


@falcon.before(check_client_accepts_json)
class CourtResource(object):

    def on_put(self, req, resp, uuid):
        data = json.load(req.stream)
        resp.body = json.dumps({
            'status': 'created',
            'uuid': uuid,
            'name': data['name'],
            'slug': data['slug']
        })
        resp.location = 'https://www.preview.alphagov.co.uk/courts/{}'.format(data['slug'])
        resp.status = falcon.HTTP_201
