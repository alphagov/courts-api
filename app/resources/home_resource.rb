class HomeResource < Webmachine::Resource
  def to_html
    <<-HTML
      <h1>Hi.</h1>
      <a href="/courts">See the courts.</a>
    HTML
  end
end
