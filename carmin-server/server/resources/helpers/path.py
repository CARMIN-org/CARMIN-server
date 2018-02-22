import os
import tarfile
import tempfile
import zipfile
import mimetypes
import hashlib
import base64
from flask import Response, make_response
from server import app
from server.resources.models.upload_data import UploadData
from server.resources.models.path import Path, PathSchema
from server.resources.models.path_md5 import PathMD5
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageMarshaller, UNAUTHORIZED, INVALID_PATH, INVALID_ACTION,
    MD5_ON_DIR, LIST_ACTION_ON_FILE, GENERIC_ERROR, INVALID_UPLOAD_TYPE,
    ACTION_REQUIRED, INVALID_MODEL_PROVIDED)


def is_safe_path(path: str, follow_symlinks: bool = True) -> bool:
    """Checks `completePath` to ensure that it lives inside the exposed /data
    directory.
    """
    base_dir = app.config['DATA_DIRECTORY']
    if follow_symlinks:
        return os.path.realpath(path).startswith(base_dir)
    return os.path.abspath(path).startwith(base_dir)


def is_root(requested_path: str) -> bool:
    return requested_path == app.config['DATA_DIRECTORY']


def upload_file(upload_data: UploadData, requested_file_path: str) -> Response:
    raw_content = base64.decodebytes(upload_data.base64_content.encode())
    with open(requested_file_path, 'wb') as f:
        f.write(raw_content)
    path = Path.object_from_pathname(requested_file_path)
    return PathSchema().dump(path).data, 201


def upload_archive(upload_data: UploadData,
                   requested_dir_path: str) -> Response:
    try:
        raw_content = base64.decodebytes(upload_data.base64_content.encode())
    except:
        return ErrorCodeAndMessageMarshaller(INVALID_MODEL_PROVIDED), 400
    file_name = '{}.zip'.format(requested_dir_path)

    with open(file_name, 'wb') as f:
        f.write(raw_content)
    with zipfile.ZipFile(file_name, mode='r') as zf:
        zf.extractall(path=requested_dir_path)
    os.remove(file_name)
    path = Path.object_from_pathname(requested_dir_path)
    return PathSchema().dump(path).data, 201


def create_directory(requested_data_path: str) -> Response:
    try:
        os.mkdir(requested_data_path)
        response_object = Path.object_from_pathname(requested_data_path)
        file_location_header = {'Location': response_object.platform_path}
        return make_response((str(PathSchema().dump(response_object).data),
                              201, file_location_header))
    except FileExistsError:
        return ErrorCodeAndMessageMarshaller(INVALID_PATH), 401


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
