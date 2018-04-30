import pytest
from server.server_helper import create_app
from server.api import declare_api
from server.database import db as _db
from server.config import TestConfig


@pytest.yield_fixture(autouse=True, scope='session')
def app():
    from server import app
    app.config.from_object(TestConfig)
    declare_api(app)
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.yield_fixture(scope='function')
def db(app):
    _db.drop_all()
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.yield_fixture(scope='function')
def session(db):
    # connect to the database
    connection = db.engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual session to the connection
    # options = dict(bind=connection, binds={})
    options = dict(bind=connection)
    session = db.create_scoped_session(options=options)

    # overload the default session with the session above
    db.session = session

    yield session
    session.close()
    # rollback - everything that happened with the
    # session above (including calls to commit())
    # is rolled back.
    transaction.rollback()
    # return connection to the Engine
    connection.close()


@pytest.fixture()
def test_client(app):
    return app.test_client()
