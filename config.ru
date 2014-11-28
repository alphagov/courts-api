$LOAD_PATH.unshift(File.dirname(__FILE__))

require 'boot'

run Courts::Application.adapter
