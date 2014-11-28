$LOAD_PATH.unshift(File.join(File.dirname(__FILE__), 'lib'))

ENV['RACK_ENV'] ||= 'development'

require 'rubygems'
require 'bundler/setup'
require 'webmachine'
require 'webmachine/adapters/rack'

require 'form_values'
require 'app/models'
require 'app/resources'

require 'application'
