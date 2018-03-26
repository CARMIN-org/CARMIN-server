from server.server_helper import create_app
from server.api import declare_api

app = create_app()

from server.logging.setup import log_response, log_exception


def main():
    declare_api(app)
    start_up()
    app.run(host='0.0.0.0', port=int(8080))


from server.startup_validation import start_up
