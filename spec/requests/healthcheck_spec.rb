require 'rails_helper'

describe 'healthcheck path' do
  it 'responds with "OK"' do
    get '/healthcheck'
    expect(response).to have_http_status(200)
    expect(response.body).to eq('OK')
  end
end
