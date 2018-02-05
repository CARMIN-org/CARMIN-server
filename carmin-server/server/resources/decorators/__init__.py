from functools import wraps
from flask_restful import request
from flask import abort
from server.resources.models.error_code_and_message import ErrorCodeAndMessage, ErrorCodeAndMessageSchema
from server.database.models.user import User

_error_code_and_message_schema = ErrorCodeAndMessageSchema()


def marshal_request(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not schema:
                return func(*args, **kwargs)
            if schema:
                body = request.get_json(force=True)
                model, errors = schema.load(body)

                if (errors):
                    return _error_code_and_message_schema.dump(
                        ErrorCodeAndMessage(
                            error_code=400,
                            error_message="Invalid model provided",
                            error_detail=errors)).data, 400

                return func(model=model, *args, **kwargs)

        return wrapper

    return decorator


def marshal_response(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            model = func(*args, **kwargs)

            if (isinstance(model, ErrorCodeAndMessage)):
                json, errors = _error_code_and_message_schema.dump(model)
                return json, model.error_code

            json, errors = schema.dump(model)

            if (errors):
                error_message = "Server error while dumping model of type %s" % type(
                    model).__name__
                return _error_code_and_message_schema.dump(
                    ErrorCodeAndMessage(
                        error_code=500,
                        error_message=error_message,
                        error_detail=errors)).data, 500

            return json

        return wrapper

    return decorator


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        apiKey = request.headers.get("apiKey")
        if (apiKey is None):
            return unauthorized_response("Missing HTTP header field apiKey")

        user = User.query.filter_by(api_key=apiKey).first()

        if not user:
            return unauthorized_response("Invalid apiKey")

    return wrapper


def unauthorized_response(msg: str):
    return _error_code_and_message_schema.dump(
        ErrorCodeAndMessage(error_code=401, error_message=msg)).data, 401