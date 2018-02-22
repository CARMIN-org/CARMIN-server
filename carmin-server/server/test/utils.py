import json
from server import app, db
from server.resources.models.error_code_and_message import ErrorCodeAndMessage, ErrorCodeAndMessageSchema
from flask import Response
from server.config import TestConfig


class TestConfigEncapsulated:
    def __init__(self, test_client, db):
        self.test_client = test_client
        self.db = db


def get_test_config():
    app.config.from_object(TestConfig)
    test_client = app.test_client()

    db.drop_all()
    db.create_all()

    db.session = db.create_scoped_session()

    return TestConfigEncapsulated(test_client, db)


def json_request_data(data):
    return json.dumps(data)


def load_json_data(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


def error_from_response(response: Response) -> ErrorCodeAndMessage:
    return ErrorCodeAndMessageSchema().load(load_json_data(response)).data
