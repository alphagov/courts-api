require 'spec_helper'

describe CourtResource do
  include Webmachine::Test

  let(:app) { Courts::Application }

  describe 'GET /courts/<id>' do
    let(:court_id) { 1 }

    before do
      get "/courts/#{court_id}", headers: {'Accept' => accept}
    end

    context 'when text/html is requested' do
      let(:accept) { 'text/html' }

      context 'id is valid' do
        it 'succeeds' do
          response.code.should == 200
        end

        it 'replies with a content type of text/html' do
          response.headers['Content-Type'].should == 'text/html'
        end

        describe 'the response body' do
          it 'includes the court name' do
            response.body.should include('Court 1')
          end

          it 'links to itself' do
            response.body.should include('<link href="/courts/1" rel="self">')
          end
        end
      end

      context 'id is invalid' do
        let(:court_id) { 11 } # we only have 10 courts in this example

        it '404s' do
          response.code.should == 404
        end
      end
    end

    context 'when JSON is requested' do
      require 'json'

      let(:accept)   { 'application/json' }

      it 'succeeds' do
        response.code.should == 200
      end

      describe 'the JSON' do
        subject(:json) { JSON.parse(response.body) }

        it 'has the court id' do
          json['id'].should == 1
        end

        it 'has the court name' do
          json['name'].should == 'Court 1'
        end
      end
    end
  end
end


