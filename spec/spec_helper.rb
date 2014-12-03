ENV['RACK_ENV'] = 'test'

$LOAD_PATH.unshift(File.join(File.dirname(__FILE__), '..'))

require 'webmachine/test'

require 'boot'
