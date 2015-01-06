import falcon

import courts


courts_api = application = falcon.API()

courts_index = courts.CourtsResource()
court = courts.CourtResource()

courts_api.add_route('/courts', courts_index)
courts_api.add_route('/courts/{uuid}', court)
