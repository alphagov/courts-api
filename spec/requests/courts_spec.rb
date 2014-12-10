require 'rails_helper'

describe 'publishing a court' do
  let(:court_json) {
    {"name" => "Barnsley Squash Court"}.to_json
  }

  it 'responds with a success code' do
    put '/courts/0c833dee-01de-4f4d-9b2e-e7d1b8d76418', court_json
    expect(response).to be_success
  end

  it 'includes the court name in the response' do
    put '/courts/0c833dee-01de-4f4d-9b2e-e7d1b8d76418', court_json
    response_json = JSON.parse(response.body)
    expect(response_json).to include("name")
    expect(response_json["name"]).to eq("Barnsley Squash Court")
  end
end
