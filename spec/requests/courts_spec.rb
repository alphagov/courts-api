require 'rails_helper'

describe 'publishing a court' do

  let(:court_json) do
    {"name" => "Barnsley Squash Court", "slug" => "barnsley-squash-court"}.to_json
  end

  let(:publishing_api_hash) do
    {
      "base_path" => "/courts/barnsley-squash-court",
      "content_id" => court_id,
      "title" => "Barnsley Squash Court",
      "format" => "court",
      "update_type" => "major",
      "publishing_app" => "courts-api",
      "rendering_app" => "courts-frontend",
      "routes" => [
        {
          "path" => "/courts/barnsley-squash-court",
          "type" => "exact",
        }
      ]
    }
  end

  let(:court_id) { '0c833dee-01de-4f4d-9b2e-e7d1b8d76418' }

  before :each do
    allow(CourtsAPI.publishing_api).to receive(:put_content_item)
  end

  it 'responds with a success code' do
    put "/courts/#{court_id}", court_json
    expect(response).to be_success
  end

  it 'sends the court to the publishing API' do
    expect(CourtsAPI.publishing_api).to receive(:put_content_item).with(
      "/courts/barnsley-squash-court",
      publishing_api_hash
    )

    put "/courts/#{court_id}", court_json
  end

  it 'includes the court name in the response' do
    put "/courts/#{court_id}", court_json
    response_json = JSON.parse(response.body)
    expect(response_json).to include("name")
    expect(response_json["name"]).to eq("Barnsley Squash Court")
  end

  it 'includes the published URL in the response' do
    put "/courts/#{court_id}", court_json
    response_json = JSON.parse(response.body)
    expect(response_json).to include("public_url")
    expect(response_json["public_url"]).to eq('https://www.gov.uk/courts/barnsley-squash-court')
  end

  it 'requires a name' do
    put "/courts/#{court_id}", {"slug" => "barnsley-squash-court"}.to_json
    expect(response).to be_unprocessable
  end

  it 'requires a slug' do
    put "/courts/#{court_id}", {"name" => "Barnsley Squash Court"}.to_json
    expect(response).to be_unprocessable
  end

  it 'returns 400 for invalid JSON' do
    put "/courts/#{court_id}", '{"trailing": "comma",}'
    expect(response).to be_bad_request
  end
end
