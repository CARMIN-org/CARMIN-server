import random
import json
from server import db
from flask_restful import Resource, fields, request
from flask import make_response, jsonify, abort
from .models.authentication import Authentication, AuthenticationSchema
from .models.authentication_credentials import AuthenticationCredentials, AuthenticationCredentialsSchema
from server.common.error_codes_and_messages import INVALID_USERNAME_OR_PASSWORD
from server.database.models.user import User
from .decorators import unmarshal_request, marshal_response, get_db_session
from server.common.util import generate_api_key


class Authenticate(Resource):
    @get_db_session
    @unmarshal_request(AuthenticationCredentialsSchema())
    @marshal_response(AuthenticationSchema())
    def post(self, model, db_session):
        user = db_session.query(User).filter_by(
            username=model.username, password=model.password).first()

        if not user:
            return INVALID_USERNAME_OR_PASSWORD

        if (user.api_key is None):
            user.api_key = generate_api_key()
            db_session.add(user)
            db_session.commit()

        result = Authentication(
            http_header="apiKey", http_header_value=user.api_key)
        return result
