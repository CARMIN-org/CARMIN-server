"""
Launching Flask
"""
import os
from flask import Flask

APP = Flask(__name__)


@APP.route("/")
def hello():
    """ Simple Hello World function for testing """
    return "Hello, World!"


if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=int(os.environ["SERVER_PORT"]))
