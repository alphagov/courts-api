require 'ostruct'

class User < OpenStruct
  include GDS::SSO::User

  def self.where(*args)
    []
  end

  def self.first
    new
  end

  def update_attribute(key, value)
    public_send("#{key}=", value)
  end

  def self.create!(args)
    new(args)
  end
end
