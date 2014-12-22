namespace :router do
  task :router_environment => :environment do
    require 'plek'
    require 'gds_api/router'

    @router_api = GdsApi::Router.new(Plek.current.find('router-api'))
  end

  task :register_routes => :router_environment do
    @router_api.add_redirect_route('/courts', 'exact', '/find-court-tribunal', 'temporary', commit: true)
  end

  desc 'Register courts-frontend application and routes with the router'
  task :register => [ :register_routes ]
end
