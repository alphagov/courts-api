require 'webmachine'

module Courts
  Application = Webmachine::Application.new do |app|
    app.configure do |config|
      config.adapter = :Rack
    end
    app.inject_resource_url_provider
  end

  require 'config/routes'
end

