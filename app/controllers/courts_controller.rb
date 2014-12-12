class CourtsController < ApplicationController
  before_filter :parse_request_body, only: [:update]

  def update
    unless court_body['name'].present? && court_body["slug"].present?
      return head :unprocessable_entity
    end

    publishing_api_body = publishing_api_format(params[:id], court_body)

    CourtsAPI.publishing_api.put_content_item(
      base_path(court_body),
      publishing_api_body,
    )
    render json: {
      name: court_body["name"],
      public_url: (Plek.new.website_uri + base_path(court_body)).to_s
    }
  end

private
  def court_body
    @parsed_request_body
  end

  def base_path(court_body)
    "/courts/#{court_body["slug"]}"
  end

  def publishing_api_format(court_id, court_body)
    name = court_body["name"]

    {
      base_path: base_path(court_body),
      content_id: court_id,
      title: name,
      format: "court",
      update_type: "major",
      publishing_app: "courts-api",
      rendering_app: "courts-frontend",
      routes: [
        { path: base_path(court_body), type: "exact" }
      ]
    }
  end
end
