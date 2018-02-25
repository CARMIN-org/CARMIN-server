import os
from flask import Response
from .path import create_directory, get_user_data_directory, is_safe_path
from server import app
from server.database.models.user import User
from server.resources.models.path import Path
from server.resources.models.authentication_credentials import AuthenticationCredentials
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import UNAUTHORIZED, PATH_EXISTS, USERNAME_ALREADY_EXISTS


def create_user_directory(user: User) -> (Path, ErrorCodeAndMessage):
    user_dir_absolute_path = get_user_data_directory(user)

    if not is_safe_path(user_dir_absolute_path):
        return None, UNAUTHORIZED

    return create_directory(user_dir_absolute_path)
