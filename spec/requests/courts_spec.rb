require 'rails_helper'


describe 'publishing a court' do
  Given(:court_id) { '0c833dee-01de-4f4d-9b2e-e7d1b8d76418' }

  Given(:court_json) do
    { name: 'Barnsley Squash Court', slug: 'barnsley-squash-court' }.to_json
  end

  When { put "/courts/#{court_id}", court_json }

  context 'the happy path' do
    Given(:publishing_api_hash) do
      {
        base_path: '/courts/barnsley-squash-court',
        content_id: court_id,
        title: 'Barnsley Squash Court',
        format: 'court',
        update_type: 'major',
        publishing_app: 'courts-api',
        rendering_app: 'courts-frontend',
        routes: [
                     {
                       path: '/courts/barnsley-squash-court',
                       type: 'exact',
                     }
                   ]
      }
    end

    Given { allow(CourtsAPI.publishing_api).to receive(:put_content_item).with(
                                                 '/courts/barnsley-squash-court',
                                                 publishing_api_hash)
          }

    Then { response.code == '200' }

    let(:response_json) { JSON.parse(response.body) }

    Then { response_json['name']       == 'Barnsley Squash Court' }
    Then { response_json['public_url'] == 'https://www.gov.uk/courts/barnsley-squash-court' }
  end

  context 'the unhappy endings' do
    When { put "/courts/#{court_id}", court_json }

    context 'no name is given' do
      Given(:court_json) { { slug: 'barnsley-squash-court' }.to_json }
      Then { response.code == '422' }
    end

    context 'no slug is given' do
      Given(:court_json) { { name: 'Barnsley Squash Court' }.to_json }
      Then { response.code == '422' }
    end

    context 'invalid JSON' do
      Given(:court_json) { '{"trailing": "comma",}' }
      Then { response.code == '400' }
    end
  end
end
