# We're doing our own JSON parsing, and error handling. Rails by default tries
# to parse the request body when the Content-Type header is application/json.
# When given invalid json, it then blows up before even reaching the
# application, preventing us from handling invalid json gracefully. This
# disables the default behaviour, allowing us to handle this case ourselves.
Rails.application.config.middleware.delete "ActionDispatch::ParamsParser"
