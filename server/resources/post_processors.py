from server import app


@app.after_request
def set_content_length_to_0(response):
    """This is a bug in the current version of Flask. All 204 responses with
    no body returns a Content-Length of 3, which causes problems with the
    connection expectations. This function sets Content-Length to 0 for all
    204 responses with no body."""
    if (response.status_code == 204
            and response.headers.get('Content-Length') != '0'
            and response.data == b'""\n'):
        response.headers['Content-Length'] = 0
    return response
