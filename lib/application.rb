require 'webmachine'

module Courts
  Application = Webmachine::Application.new do |app|
    app.configure do |config|
      config.adapter = :Rack
    end
  end

  require 'config/routes'
end

