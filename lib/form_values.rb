require 'cgi'

module FormValues
  def form_values
    request.body.to_s.split("\n").inject({}) do |hash, line|
      key, value = line.split('=')
      value = CGI::unescape(value) if value
      hash[key] = value
      hash
    end
  end
end
