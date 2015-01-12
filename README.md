# MOJ Courts and Tribunals API

This app provides URLs for publishing MOJ courts and tribunals information to
GOV.UK.

* [API specification](doc/api-specification.md)

# Development

This branch is a quick sketch using [Falcon](http://falconframework.org/) and
[jsonschema](https://github.com/Julian/jsonschema). To run this locally, create
a new virtualenv and then:

```
pip install -r requirements.txt
gunicorn --reload --access-logfile - --error-logfile - courts_api.app
```

## Current behaviour

Make requests using [HTTPie](https://github.com/jakubroztocil/httpie):

```
# Make a GET request for all courts (currently hard-coded):
http localhost:8000/courts
# 200 OK

# PUT a valid court:
http PUT localhost:8000/courts/123 name='Barnsley Court', slug='barnsley-court'
# 201 Created, with body containing data parsed from the request

# PUT an invalid court:
http PUT localhost:8000/courts/123 name='Barnsley Court', foo='bar'
# 422 Unacceptable Entity, with error messages from validation

# PUT a valid court, but only accepting XML:
http PUT localhost:8000/courts/123 name='Barnsley Court', slug='barnsley-court'  Accept:application/xml
# 406 Not Acceptable

# Try to GET a court:
http GET localhost:8000/courts/123
# 405 Method Not Allowed
```
