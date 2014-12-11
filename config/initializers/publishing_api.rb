require 'gds_api/publishing_api'

CourtsAPI.publishing_api = GdsApi::PublishingApi.new(Plek.current.find('publishing-api'))
