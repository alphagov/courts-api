require 'spec_helper'

describe CourtsResource do
  include Webmachine::Test

  let(:app) { Courts::Application }

  describe 'GET /courts' do
    before do
      get '/courts'
    end

    it 'succeeds' do
      response.code.should == 200
    end

    it 'replies with a content type of text/html' do
      response.headers['Content-Type'].should == 'text/html'
    end

    describe 'the response body' do
      it 'includes a list of courts' do
        response.body.should include('<ul class="courts">')
      end

      it 'has a form to create new courts' do
        response.body.should include('<form method="POST" action="/courts">')
      end
    end
  end

  describe 'POST /courts' do
    before do
      post '/courts',
           headers: { 'Content-Type' => 'application/x-www-form-urlencoded' },
           body:    "court_name=#{court_name}"

    end

    context 'the court name is valid' do
      let(:court_name) { 'A new court' }

      it 'creates a new court' do
        response.code.should == 201
      end

      it 'gives an absolute URL to it' do
        response.headers['Location'].should == 'http://localhost/courts/A+new+court'
      end
    end

    context 'the court name is invalid' do
      let(:court_name) { 'Invalid court name' }

      it 'is a bad request' do
        response.code.should == 400
      end

      it 'says why' do
        response.body.should include('We only accept "A new court" as a new court name')
      end
    end
  end
end


