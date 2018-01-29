from functools import wraps
from flask_restful import request
from flask import abort


def resource_model(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not schema:
                return func(*args, **kwargs)
            if schema:
                body = request.get_json(force=True)
                model, errors = schema.load(body)

                if (errors):
                    return abort(400, errors)

                return func(model=model, *args, **kwargs)

        return wrapper

    return decorator


def custom_marshal_with(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            model = func(*args, **kwargs)
            json, errors = schema.dump(model)

            return json

        return wrapper

    return decorator