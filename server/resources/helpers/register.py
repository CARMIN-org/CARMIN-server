import os
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from .path import create_directory, get_user_data_directory, is_safe_path
from server.database.models.user import User, Role
from server.resources.models.path import Path
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, UNAUTHORIZED, USERNAME_ALREADY_EXISTS,
    UNEXPECTED_ERROR)


def create_user_directory(user: User) -> ErrorCodeAndMessage:
    user_dir_absolute_path = get_user_data_directory(user.username)

    if not is_safe_path(user_dir_absolute_path):
        return UNAUTHORIZED

    path, error = create_directory(user_dir_absolute_path, False)
    return error


def register_user(
        username: str,
        password: str,
        user_role: Role,
        db_session,
        ignore_directory_fail: bool = False) -> (bool, ErrorCodeAndMessage):
    try:
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role=user_role)

        db_session.add(new_user)
        error = create_user_directory(new_user)
        if error and not ignore_directory_fail:
            db_session.rollback()
            return False, error

        db_session.commit()
        return True, None
    except IntegrityError:
        db_session.rollback()
        return False, ErrorCodeAndMessageFormatter(USERNAME_ALREADY_EXISTS,
                                                   username)
