class ApplicationController < ActionController::API
  include GDS::SSO::ControllerMethods

private
  def check_content_type_header
    if request.headers['Content-Type'] != 'application/json'
      render json: { status: 'error', errors: 'Invalid Content-Type header. You must send application/json.' }, status: 415
    end
  end

  def check_accept_header
    if request.headers['Accept'] != 'application/json'
      render json: { status: 'error', errors: 'Invalid Accept header. You must accept application/json.' }, status: 406
    end
  end

  def parse_request_body
    @parsed_request_body = JSON.parse(request.body.read)
  rescue JSON::ParserError => e
    message = "Request JSON could not be parsed: #{e.message}"
    render json: { status: 'error', errors: [message] }, status: 400
  end
end
