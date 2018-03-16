from functools import wraps
from flask_restful import request
from flask import abort
from server.database import db
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageMarshaller, INVALID_MODEL_PROVIDED, MODEL_DUMPING_ERROR,
    MISSING_API_KEY, INVALID_API_KEY, UNAUTHORIZED, UNEXPECTED_ERROR)
from server.database.models.user import User, Role


def unmarshal_request(schema, allow_none: bool = False, partial=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not schema:
                return func(*args, **kwargs)
            if schema:
                body = request.get_json(force=True, silent=True)
                if not body:
                    if allow_none:
                        return func(model=body, *args, **kwargs)
                    else:
                        return ErrorCodeAndMessageMarshaller(
                            INVALID_MODEL_PROVIDED), 400

                model, errors = schema.load(body, partial=partial)
                if errors:
                    invalid_model_provided_error = INVALID_MODEL_PROVIDED
                    invalid_model_provided_error.error_detail = errors
                    return ErrorCodeAndMessageMarshaller(
                        invalid_model_provided_error), 400

                return func(model=model, *args, **kwargs)

        return wrapper

    return decorator


def marshal_response(schema=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            model = func(*args, **kwargs)

            if (isinstance(model, ErrorCodeAndMessage)):
                return ErrorCodeAndMessageMarshaller(
                    model), 500 if model == UNEXPECTED_ERROR else 400

            if (schema is None):
                return '', 204

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

        user = db.session.query(User).filter_by(api_key=apiKey).first()

        if not user:
            return ErrorCodeAndMessageMarshaller(INVALID_API_KEY), 401

        return func(user=user, *args, **kwargs)

    return wrapper


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        apiKey = request.headers.get("apiKey")
        if (apiKey is None):
            return ErrorCodeAndMessageMarshaller(MISSING_API_KEY), 401

        user = db.session.query(User).filter_by(api_key=apiKey).first()

        if not user:
            return ErrorCodeAndMessageMarshaller(INVALID_API_KEY), 401

        if (user.role != Role.admin):
            return ErrorCodeAndMessageMarshaller(UNAUTHORIZED), 401

        return func(user=user, *args, **kwargs)

    return wrapper
