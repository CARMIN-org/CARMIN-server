import sys
from server.server_helper import create_app
from server.api import declare_api

app = create_app()

from server.logging.setup import log_response, log_exception
from server.resources.post_processors import *


def main():
    declare_api(app)
    start_up()
    if len(sys.argv) > 1:
        port = sys.argv[1]
        try:
            port = int(port)
        except ValueError:
            print("Invalid port number. Port must be an integer.")
            exit(1)
    else:
        port = 8080
    app.run(host='0.0.0.0', port=port)


from server.startup_validation import start_up
