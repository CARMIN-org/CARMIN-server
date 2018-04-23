from flask_restful import Resource
from werkzeug.security import generate_password_hash
from server.database import db
from server.database.models.user import User, Role
from server.common.error_codes_and_messages import (
    UNAUTHORIZED, USER_DOES_NOT_EXIST, INVALID_MODEL_PROVIDED,
    ErrorCodeAndMessageFormatter, ErrorCodeAndMessageAdditionalDetails)
from .models.authentication_credentials import AuthenticationCredentialsSchema
from .decorators import marshal_response, login_required, unmarshal_request


class Edit(Resource):
    @login_required
    @unmarshal_request(AuthenticationCredentialsSchema(), partial=True)
    @marshal_response(AuthenticationCredentialsSchema())
    def post(self, model, user):
        if model.password:
            if user.role == Role.admin and model.username:
                # Logged in user is an admin and wants to change
                # another user's password
                edit_user = db.session.query(User).filter_by(
                    username=model.username).first()
                if not edit_user:
                    return ErrorCodeAndMessageFormatter(
                        USER_DOES_NOT_EXIST, model.username)
            else:
                # Logged in user is not an admin
                if model.username and model.username != user.username:
                    return UNAUTHORIZED
                edit_user = db.session.query(User).filter_by(
                    username=user.username).first()
            edit_user.password = generate_password_hash(model.password)
            db.session.commit()
        else:
            # Password was not provided
            return ErrorCodeAndMessageAdditionalDetails(
                INVALID_MODEL_PROVIDED, "'password' is required")
