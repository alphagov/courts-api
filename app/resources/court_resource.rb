class CourtResource < Webmachine::Resource
  include Webmachine::Linking::Resource::LinkHelpers

  def allowed_methods
    %w(GET PUT DELETE)
  end

  def content_types_accepted
    %w(application/json)
  end

  def content_types_provided
    [
      ['text/html', :to_html],
      ['application/json', :to_json]
    ]
  end

  def resource_exists?
    @court = Court.find(id)
  end

  def delete_resource
    @court.close!
  end

  def from_json
    @court.update(params)
    response.body = @court.to_json
  end

  def to_json
    @court.to_json
  end

  def to_html
    <<-HTML
      <html>
        <head>
          #{link_tag('self', CourtResource, id: id)}
        </head>
      <body>
      <h1>#{@court.name}</h1>
      <p>Lorem ipsum justice, um</p>
      </body>
      <html>
    HTML
  end

private
  def id
    request.path_info[:id].to_i
  end

  def params
    JSON.parse(request.body.to_s)
  end
end
