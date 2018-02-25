from server import db
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from .models.authentication_credentials import AuthenticationCredentials, AuthenticationCredentialsSchema
from server.common.error_codes_and_messages import USERNAME_ALREADY_EXISTS
from server.database.models.user import User, Role
from .decorators import admin_only, unmarshal_request, marshal_response, get_db_session
from server.resources.helpers.register import create_user_directory
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, USERNAME_ALREADY_EXISTS, UNEXPECTED_ERROR)


class Register(Resource):
    @admin_only
    @get_db_session
    @unmarshal_request(AuthenticationCredentialsSchema())
    @marshal_response()
    def post(self, model, db_session, user):
        already_existing_user = db_session.query(User).filter_by(
            username=model.username).first()

        if already_existing_user:
            return ErrorCodeAndMessageFormatter(USERNAME_ALREADY_EXISTS, model)

        try:
            new_user = User(
                username=model.username,
                password=model.password,
                role=Role.user)

            db_session.add(new_user)
            path, error = create_user_directory(new_user)
            if (error):
                db_session.rollback()
                return UNEXPECTED_ERROR

            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            return ErrorCodeAndMessageFormatter(USERNAME_ALREADY_EXISTS, model)
