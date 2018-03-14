import json
from flask import Response
from server.resources.models.error_code_and_message import ErrorCodeAndMessage, ErrorCodeAndMessageSchema


def load_json_data(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


def error_from_response(response: Response) -> ErrorCodeAndMessage:
    return ErrorCodeAndMessageSchema().load(load_json_data(response)).data
