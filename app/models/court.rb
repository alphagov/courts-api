class Court < Struct.new(:id)
  # There are only 10 courts in our example.
  # Except for negative courts. Don't do that.
  def self.find(id)
    Court.new(id) unless id > 10
  end

  def close!
    true
  end

  def update(params)
    true
  end

  def name
    "Court #{id}"
  end
end
