import os
import json
import tarfile
import tempfile
import mimetypes
import hashlib
from typing import List
from flask_restful import Resource, request
from flask import send_file, Response
from server import app
from server.common.error_codes_and_messages import ErrorCodeAndMessageMarshaller, UNAUTHORIZED, INVALID_PATH, INVALID_ACTION, MD5_ON_DIR, LIST_ACTION_ON_FILE
from .models.error_code_and_message import ErrorCodeAndMessageSchema
from .models.path_md5 import PathMD5, PathMD5Schema
from .models.path import Path as PathModel
from .models.path import PathSchema


class Path(Resource):
    """Allow file downloading and give access to multiple information about a
    specific path. The response format and content depends on the mandatory action
    query parameter (see the parameter description).
    Basically, the `content` action downloads the raw file, and the other actions
    return various informations in JSON.
    """

    def get(self, complete_path: str = ''):
        """The @marshal_response() decorator is not used since this method can return
        a number of different Schemas or binary content. Use `return schema.dump()`
        instead, where `schema` is the Schema of the class to be returned.
        """

        action = request.args.get('action', '')
        data_path = app.config['DATA_DIRECTORY']
        requested_data_path = os.path.realpath(
            os.path.join(data_path, complete_path))

        if not is_safe_path(data_path, requested_data_path):
            return ErrorCodeAndMessageMarshaller(UNAUTHORIZED)

        if not os.path.exists(requested_data_path):
            return ErrorCodeAndMessageMarshaller(INVALID_PATH)

        if action == 'content':
            return content_action(requested_data_path)
        elif action == 'properties':
            path = properties_action(data_path, complete_path)
            return PathSchema().dump(path)
        elif action == 'exists':
            pass
        elif action == 'list':
            if not os.path.isdir(requested_data_path):
                return ErrorCodeAndMessageMarshaller(LIST_ACTION_ON_FILE)
            directory_list = list_action(data_path, complete_path)
            return PathSchema(many=True).dump(directory_list)
        elif action == 'md5':
            if os.path.isdir(requested_data_path):
                return ErrorCodeAndMessageMarshaller(MD5_ON_DIR)
            md5 = PathMD5(generate_md5(requested_data_path))
            return PathMD5Schema().dump(md5)
        else:
            return ErrorCodeAndMessageMarshaller(INVALID_ACTION)

    def put(self, complete_path):
        pass

    def delete(self, complete_path):
        pass


def content_action(complete_path: str) -> Response:
    if os.path.isdir(complete_path):
        tarball = make_tarball(complete_path)
        response = send_file(
            tarball, mimetype="application/gzip", as_attachment=True)
        os.remove(tarball)
        return response
    mimetype, _ = mimetypes.guess_type(complete_path)
    response = send_file(complete_path)
    if mimetype:
        response.mimetype = mimetype
    return response


def properties_action(platform_data_path: str,
                      requested_file_path: str) -> Path:
    return PathModel.object_from_pathname(platform_data_path,
                                          requested_file_path)


def list_action(platform_data_path: str,
                relative_path_to_resource: str) -> List[Path]:
    result_list = []
    absolute_path_to_resource = os.path.join(platform_data_path,
                                             relative_path_to_resource)
    directory_list = os.listdir(absolute_path_to_resource)
    for f_d in directory_list:
        if not f_d.startswith('.'):
            result_list.append(
                PathModel.object_from_pathname(platform_data_path,
                                               os.path.join(
                                                   relative_path_to_resource,
                                                   f_d)))
    return result_list


def make_tarball(data_path: str) -> tarfile:
    temp_file = os.path.join(tempfile.gettempdir(),
                             os.path.basename(data_path)) + ".tar.gz"
    with tarfile.open(temp_file, mode='w:gz') as archive:
        archive.add(data_path, arcname=os.path.basename(data_path))
    return temp_file


def is_safe_path(basedir: str, path: str,
                 follow_symlinks: bool = True) -> bool:
    """Checks `completePath` to ensure that it lives inside the exposed /data
    directory.
    """
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    return os.path.abspath(path).startwith(basedir)


def generate_md5(data_path: str) -> PathMD5:
    hash_md5 = hashlib.md5()
    with open(data_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
