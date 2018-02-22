from server import db
from flask_restful import Resource
from .models.authentication_credentials import AuthenticationCredentials, AuthenticationCredentialsSchema
from server.common.error_codes_and_messages import USERNAME_ALREADY_EXISTS
from server.database.models.user import User, Role
from .decorators import admin_only, marshal_request, marshal_response


class Register(Resource):
    @admin_only
    @marshal_request(AuthenticationCredentialsSchema())
    @marshal_response()
    def post(self, model, user):
        already_existing_user = User.query.filter_by(
            username=model.username).first()

        if already_existing_user:
            error_code_and_message = USERNAME_ALREADY_EXISTS
            error_code_and_message.error_message = USERNAME_ALREADY_EXISTS.error_message.format(
                model.username)
            return error_code_and_message

        new_user = User(
            username=model.username, password=model.password, role=Role.user)
        db.session.add(new_user)
        db.session.commit()
