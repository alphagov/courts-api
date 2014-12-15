require 'rails_helper'

describe 'publishing a court' do
  let(:court_id) { '0c833dee-01de-4f4d-9b2e-e7d1b8d76418' }

  before do
    allow(CourtsAPI.publishing_api).to receive(:put_content_item)
    put "/courts/#{court_id}", court_json
  end

  context 'the happy path' do
    let(:court_json) do
      { name: 'Barnsley Squash Court', slug: 'barnsley-squash-court' }.to_json
    end

    let(:publishing_api_hash) do
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

    let(:response_json) { JSON.parse(response.body) }

    it 'responds with a success code' do
      expect(response).to have_http_status(200)
    end

    it 'sends the court to the publishing API' do
      expect(CourtsAPI.publishing_api).to have_received(:put_content_item).with(
                                            '/courts/barnsley-squash-court',
                                            publishing_api_hash
                                          )
    end

    it 'includes the court name in the response' do
      expect(response_json['name']).to eq('Barnsley Squash Court')
    end

    it 'includes the published URL in the response' do
      expect(response_json['public_url']).to eq('https://www.gov.uk/courts/barnsley-squash-court')
    end
  end

  context 'the unhappy endings' do
    context 'no name is given' do
      let(:court_json) { { slug: 'barnsley-squash-court' }.to_json }
      it('is unprocessable') { expect(response).to have_http_status(422) }
    end

    context 'no slug is given' do
      let(:court_json) { { name: 'Barnsley Squash Court' }.to_json }
      it('is unprocessable') { expect(response).to have_http_status(422) }
    end

    context 'the JSON is invalid' do
      let(:court_json) { '{"trailing": "comma",}' }
      it('is a bad request') { expect(response).to have_http_status(400) }
    end
  end
end
