class CourtsResource < Webmachine::Resource
  include FormValues

  def allowed_methods
    %w(GET POST)
  end

  def post_is_create?
    true
  end

  def create_path
    "/courts/#{CGI::escape(new_court_name)}"
  end

  def content_types_accepted
    [
      ['application/x-www-form-urlencoded', :from_form],
      ['application/json',                  :from_json],
    ]
  end

  def from_form
    if new_court_name != 'A new court'
      raise Webmachine::MalformedRequest, 'We only accept "A new court" as a new court name'
    end
  end

  def from_json
    403 # ho, ho
  end

  def to_html
    <<-HTML
      <h1>Courts</h1>
      <ul class="courts">
        <li><a href='/courts/1'>Court 1</a></li>
        <li><a href='/courts/2'>Court 2</a></li>
        <li><a href='/courts/3'>Court 3</a></li>
      </ul>

      <h2>Add a new court</h2>
      <i>(we'll take any of #{content_types_accepted.map(&:first)})</i>
      <form method="POST" action="/courts">
        <input type="text" name="court_name">
        <input type="submit">
      </form>
    HTML
  end

private
  def new_court_name
    @_new_court_name ||= form_values.fetch('court_name')
  end
end
