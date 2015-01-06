import falcon

import courts


api = application = falcon.API()

courts_index = courts.CourtsResource()
court = courts.CourtResource()

api.add_route('/courts', courts_index)
api.add_route('/courts/{uuid}', court)
