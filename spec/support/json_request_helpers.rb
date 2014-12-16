module JSONRequestHelper
  def put_json(path, attrs, headers = {})
    default_headers = {
      "CONTENT_TYPE" => "application/json",
      "ACCEPT" => "application/json",
      'HTTP_AUTHORIZATION' => 'Bearer 12345678',
    }
    put path, attrs.to_json, default_headers.merge(headers)
  end
end

RSpec.configuration.include JSONRequestHelper, :type => :request
