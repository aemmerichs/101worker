def helloName(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)
    open("resources.json", "read").read()
    return {}


def hello(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)

    return {}


def routes():
    return [
        ('/termResources/(?P<name>[^/]+)', helloName),
        ('/termResources', hello)
    ]
