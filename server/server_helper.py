from flask import Flask
from server.database import db, init_db
from server.config import Config


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    db.app = app
    init_db(db)

    return app
