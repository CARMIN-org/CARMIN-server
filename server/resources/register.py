from server.database import db
from flask_restful import Resource
from .models.authentication_credentials import AuthenticationCredentials, AuthenticationCredentialsSchema
from server.common.error_codes_and_messages import USERNAME_ALREADY_EXISTS
from .decorators import admin_only, unmarshal_request, marshal_response
from server.resources.helpers.register import register_user
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, USERNAME_ALREADY_EXISTS, UNEXPECTED_ERROR)
from server.database.models.user import User, Role


class Register(Resource):
    @admin_only
    @unmarshal_request(AuthenticationCredentialsSchema())
    @marshal_response()
    def post(self, model, user):
        already_existing_user = db.session.query(User).filter_by(
            username=model.username).first()

        if already_existing_user:
            return ErrorCodeAndMessageFormatter(USERNAME_ALREADY_EXISTS,
                                                model.username)
        result, error = register_user(model.username, model.password,
                                      Role.user, db.session)

        if error:
            if error.error_code != USERNAME_ALREADY_EXISTS.error_code:
                return UNEXPECTED_ERROR
            return error