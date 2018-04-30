import os
import json
import shutil
from flask_restful import Resource, request
from flask import Response, make_response
from server.common.utils import marshal
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, UNAUTHORIZED, INVALID_PATH, INVALID_ACTION,
    MD5_ON_DIR, LIST_ACTION_ON_FILE, ACTION_REQUIRED, UNEXPECTED_ERROR,
    PATH_IS_DIRECTORY, INVALID_REQUEST, PATH_DOES_NOT_EXIST)
from .models.upload_data import UploadDataSchema
from .models.boolean_response import BooleanResponse
from .models.path import Path as PathModel
from .models.path import PathSchema
from .decorators import login_required, unmarshal_request
from .helpers.path import (is_safe_for_delete, upload_file, upload_archive,
                           create_directory, generate_md5, is_safe_for_put,
                           is_safe_for_get, make_absolute, get_content,
                           get_path_list)


class Path(Resource):
    """Allow file downloading and give access to multiple information about a
    specific path. The response format and content depends on the mandatory action
    query parameter (see the parameter description).
    Basically, the `content` action downloads the raw file, and the other actions
    return various informations in JSON.
    """

    @login_required
    def get(self, user, complete_path: str = ''):
        """The @marshal_response() decorator is not used since this method can return
        a number of different Schemas or binary content. Use `response(Model)`
        instead, where `Model` is the object to be returned.
        """

        action = request.args.get('action', default='', type=str).lower()
        requested_data_path = make_absolute(complete_path)

        if not is_safe_for_get(requested_data_path, user):
            return marshal(INVALID_PATH), 401

        if not os.path.exists(requested_data_path) and action != 'exists':
            return marshal(PATH_DOES_NOT_EXIST), 401

        if not action:
            return marshal(ACTION_REQUIRED), 400

        if action == 'content':
            return get_content(requested_data_path)
        elif action == 'properties':
            path = PathModel.object_from_pathname(requested_data_path)
            return marshal(path)
        elif action == 'exists':
            path_exists = os.path.exists(requested_data_path)
            return marshal(BooleanResponse(path_exists))
        elif action == 'list':
            if not os.path.isdir(requested_data_path):
                return marshal(LIST_ACTION_ON_FILE), 400
            directory_list = get_path_list(complete_path)
            return marshal(directory_list)
        elif action == 'md5':
            if os.path.isdir(requested_data_path):
                return marshal(MD5_ON_DIR), 400
            md5 = generate_md5(requested_data_path)
            return marshal(md5)
        else:
            return marshal(INVALID_ACTION), 400

    @login_required
    @unmarshal_request(UploadDataSchema(), allow_none=True)
    def put(self, user, model, complete_path: str = ''):
        requested_data_path = make_absolute(complete_path)

        if not is_safe_for_put(requested_data_path, user):
            return marshal(INVALID_PATH), 401

        if not model:
            path, error = create_directory(requested_data_path)
            if error:
                return marshal(error), 400
            file_location_header = {'Location': path.platform_path}
            string_path = json.dumps(PathSchema().dump(path).data)
            return make_response((string_path, 201, file_location_header))

        if model.upload_type == "File":
            if os.path.isdir(requested_data_path):
                error = ErrorCodeAndMessageFormatter(PATH_IS_DIRECTORY,
                                                     complete_path)
                return marshal(error), 400
            path, error = upload_file(model, requested_data_path)
            if error:
                return marshal(error), 400
            return marshal(path), 201

        if model.upload_type == "Archive":
            path, error = upload_archive(model, requested_data_path)
            if error:
                return marshal(error), 400
            return marshal(path), 201

        return marshal(INVALID_REQUEST), 400

    @login_required
    def delete(self, user, complete_path: str = ''):
        requested_data_path = make_absolute(complete_path)

        if not is_safe_for_delete(requested_data_path, user):
            return marshal(UNAUTHORIZED), 403

        if os.path.isdir(requested_data_path):
            shutil.rmtree(requested_data_path, ignore_errors=True)
        else:
            try:
                os.remove(requested_data_path)
            except FileNotFoundError:
                return marshal(PATH_DOES_NOT_EXIST), 400
            except OSError:
                return marshal(UNEXPECTED_ERROR), 500
        return Response(status=204)
