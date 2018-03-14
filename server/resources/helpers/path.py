import os
import tarfile
import tempfile
import zipfile
import mimetypes
import hashlib
import base64
from binascii import Error
from flask import Response, make_response
from server import app
from server.resources.models.upload_data import UploadData
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.database.models.user import User, Role
from server.resources.models.path import Path, PathSchema
from server.resources.models.path_md5 import PathMD5
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageMarshaller, INVALID_PATH, PATH_EXISTS,
    INVALID_MODEL_PROVIDED, NOT_AN_ARCHIVE, INVALID_BASE_64)
from .executions import EXECUTIONS_DIRNAME


def is_safe_path(path: str, follow_symlinks: bool = True) -> bool:
    """Checks `completePath` to ensure that it lives inside the exposed /data
    directory.
    """
    base_dir = app.config['DATA_DIRECTORY']
    if follow_symlinks:
        return os.path.realpath(path).startswith(base_dir)
    return os.path.abspath(path).startwith(base_dir)


def is_data_accessible(path: str, user: User) -> bool:
    if user.role == Role.admin:
        return True
    return os.path.realpath(path).startswith(
        get_user_data_directory(user.username))


def is_execution_dir(path: str, username: str) -> bool:
    user_execution_dir = os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME)
    return os.path.realpath(path).startswith(user_execution_dir)


def get_user_data_directory(username: str) -> str:
    return os.path.join(app.config['DATA_DIRECTORY'], username)


def is_safe_for_delete(requested_path: str, username: str) -> bool:
    return not requested_path == get_user_data_directory(username)


def upload_file(upload_data: UploadData,
                requested_file_path: str) -> (Path, ErrorCodeAndMessage):
    try:
        raw_content = base64.decodebytes(upload_data.base64_content.encode())
    except Error as e:
        error_code_and_message = INVALID_BASE_64
        error_code_and_message.error_message = INVALID_BASE_64.error_message.format(
            e)
        return None, error_code_and_message
    with open(requested_file_path, 'wb') as f:
        f.write(raw_content)
    path = Path.object_from_pathname(requested_file_path)
    return path, None


def upload_archive(upload_data: UploadData,
                   requested_dir_path: str) -> (Path, ErrorCodeAndMessage):
    try:
        raw_content = base64.decodebytes(upload_data.base64_content.encode())
    except Error as e:
        error_code_and_message = INVALID_BASE_64
        error_code_and_message.error_message = INVALID_BASE_64.error_message.format(
            e)
        return None, error_code_and_message
    file_name = '{}.zip'.format(requested_dir_path)

    with open(file_name, 'wb') as f:
        f.write(raw_content)
    try:
        with zipfile.ZipFile(file_name, mode='r') as zf:
            zf.extractall(path=requested_dir_path)
    except zipfile.BadZipFile as e:
        error_code_and_message = NOT_AN_ARCHIVE
        error_code_and_message.error_message = NOT_AN_ARCHIVE.error_message.format(
            e)
        return None, error_code_and_message
    os.remove(file_name)
    path = Path.object_from_pathname(requested_dir_path)
    return path, None


def create_directory(requested_data_path: str) -> (Path, ErrorCodeAndMessage):
    try:
        os.mkdir(requested_data_path)
        return Path.object_from_pathname(requested_data_path), None
    except FileExistsError:
        return None, PATH_EXISTS


def generate_md5(data_path: str) -> PathMD5:
    hash_md5 = hashlib.md5()
    with open(data_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return PathMD5(hash_md5.hexdigest())


def make_tarball(data_path: str) -> tarfile:
    temp_file = os.path.join(tempfile.gettempdir(),
                             os.path.basename(data_path)) + ".tar.gz"
    with tarfile.open(temp_file, mode='w:gz') as archive:
        archive.add(data_path, arcname=os.path.basename(data_path))
    return temp_file


def parent_dir_exists(requested_data_path: str) -> bool:
    parent_directory = os.path.abspath(
        os.path.join(requested_data_path, os.pardir))
    return os.path.exists(parent_directory)


def platform_path_exists(url_root: str, platform_path: str) -> (bool, str):
    path_url = '{}path/'.format(url_root)

    if isinstance(platform_path, list):
        for path in platform_path:
            exists = os.path.exists(
                os.path.join(app.config['DATA_DIRECTORY'],
                             path[len(path_url):]))
            if not exists:
                return False, path
        return True, None
    return os.path.exists(
        os.path.join(app.config['DATA_DIRECTORY'],
                     platform_path[len(path_url):])), platform_path
