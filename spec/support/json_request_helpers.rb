module JSONRequestHelper
  def put_json(path, attrs, headers = {})
    default_headers = {
      "CONTENT_TYPE" => "application/json",
      "ACCEPT" => "application/json",
    }
    put path, attrs.to_json, default_headers.merge(headers)
  end
end

RSpec.configuration.include JSONRequestHelper, :type => :request
