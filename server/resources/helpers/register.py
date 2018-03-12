import os
from .path import create_directory, get_user_data_directory, is_safe_path
from server.database.models.user import User
from server.resources.models.path import Path
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.common.error_codes_and_messages import UNAUTHORIZED


def create_user_directory(user: User) -> (Path, ErrorCodeAndMessage):
    user_dir_absolute_path = get_user_data_directory(user.username)

    if not is_safe_path(user_dir_absolute_path):
        return None, UNAUTHORIZED

    return create_directory(user_dir_absolute_path)
