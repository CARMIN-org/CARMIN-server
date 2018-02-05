import random
import json
from server import db
from flask_restful import Resource, fields, request
from flask import make_response, jsonify, abort
from .models.authentication import Authentication, AuthenticationSchema
from .models.authentication_credentials import AuthenticationCredentials, AuthenticationCredentialsSchema
from .models.error_code_and_message import ErrorCodeAndMessage
from server.database.models.user import User
from .decorators import marshal_request, marshal_response, login_required
from server.common.util import generate_api_key


class Authenticate(Resource):
    @marshal_request(AuthenticationCredentialsSchema())
    @marshal_response(AuthenticationSchema())
    def post(self, model):
        user = User.query.filter_by(
            username=model.username, password=model.password).first()

        if not user:
            return ErrorCodeAndMessage(
                error_code=401, error_message="Invalid username/password.")

        if (user.api_key is None):
            user.api_key = generate_api_key()
            db.session.add(user)
            db.session.commit()

        result = Authentication(
            http_header="apiKey", http_header_value=user.api_key)
        return result
