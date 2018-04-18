import os
import shutil
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from .path import create_directory, get_user_data_directory, is_safe_path
from .executions import create_user_executions_dir
from server.database.models.user import User, Role
from server.resources.models.path import Path
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, UNAUTHORIZED, USERNAME_ALREADY_EXISTS,
    UNEXPECTED_ERROR)


def create_user_directory(username: str) -> (str, ErrorCodeAndMessage):
    user_dir_absolute_path = get_user_data_directory(username)

    if not is_safe_path(user_dir_absolute_path):
        return None, UNAUTHORIZED

    # First let's delete user directory in case it exists
    shutil.rmtree(user_dir_absolute_path, ignore_errors=True)

    # We can now creat the user directory
    path, error = create_directory(user_dir_absolute_path, False)
    if error:
        return None, error

    # We must also create the execution dir
    try:
        user_execution_dir = create_user_executions_dir(username)
    except OSError:
        shutil.rmtree(user_dir_absolute_path)
        return None, UNEXPECTED_ERROR

    return user_dir_absolute_path, None


def register_user(username: str, password: str, user_role: Role,
                  db_session) -> (bool, ErrorCodeAndMessage):
    try:
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role=user_role)

        db_session.add(new_user)
        path, error = create_user_directory(new_user.username)
        if error:
            db_session.rollback()
            return False, error

        db_session.commit()
        return True, None
    except IntegrityError:
        db_session.rollback()
        return False, ErrorCodeAndMessageFormatter(USERNAME_ALREADY_EXISTS,
                                                   username)
