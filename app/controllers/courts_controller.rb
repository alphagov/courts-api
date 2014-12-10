class CourtsController < ApplicationController
  def update
    court_body = JSON.parse(request.body.read)
    render json: {name: court_body["name"]}
  end
end
