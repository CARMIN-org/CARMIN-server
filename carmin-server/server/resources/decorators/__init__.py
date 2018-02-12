from functools import wraps
from flask_restful import request
from flask import abort
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import ErrorCodeAndMessageMarshaller, INVALID_MODEL_PROVIDED, MODEL_DUMPING_ERROR, MISSING_API_KEY, INVALID_API_KEY
from server.database.models.user import User


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
                    invalid_model_provided_error = INVALID_MODEL_PROVIDED
                    invalid_model_provided_error.error_detail = errors
                    return ErrorCodeAndMessageMarshaller(
                        invalid_model_provided_error), 400

                return func(model=model, *args, **kwargs)

        return wrapper

    return decorator


def marshal_response(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            model = func(*args, **kwargs)

            if (isinstance(model, ErrorCodeAndMessage)):
                return ErrorCodeAndMessageMarshaller(model), 400

            json, errors = schema.dump(model)

            if (errors):
                model_dumping_error = MODEL_DUMPING_ERROR
                model_dumping_error.error_message = "Server error while dumping model of type %s" % type(
                    model).__name__
                model_dumping_error.error_detail = errors
                return ErrorCodeAndMessageMarshaller(model_dumping_error), 500

            return json

        return wrapper

    return decorator


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        apiKey = request.headers.get("apiKey")
        if (apiKey is None):
            return ErrorCodeAndMessageMarshaller(MISSING_API_KEY), 401

        user = User.query.filter_by(api_key=apiKey).first()

        if not user:
            return ErrorCodeAndMessageMarshaller(INVALID_API_KEY), 401

    return wrapper
