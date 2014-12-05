Rails.application.routes.draw do
  with_options :format => false do |r|
    r.get '/healthcheck', :to => proc { [200, {}, ['OK']] }
  end
end
