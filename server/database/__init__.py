from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(database):
    from server.database.models.user import User
    from server.database.models.execution import Execution
    database.create_all()
