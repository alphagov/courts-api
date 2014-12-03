require 'spec_helper'

describe CourtResource do
  include Webmachine::Test

  let(:app) { Courts::Application }

  describe 'GET /courts/<id>' do
    before do
      get "/courts/#{court_id}"
    end

    context 'id is valid' do
      let(:court_id) { 1 }

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
end


