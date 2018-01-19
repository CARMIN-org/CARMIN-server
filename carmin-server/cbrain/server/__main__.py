"""
Launching Flask
"""
import os
from server import app


def main():
    """ Lauching Flask server """
    app.run(host='0.0.0.0', port=int(os.environ["SERVER_PORT"]))


if __name__ == '__main__':
    main()
