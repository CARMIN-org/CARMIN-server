import os
import json
import shutil
import tempfile
from boutiques import bosh
from typing import Dict
from server import app
from server.database.models.user import User, Role
from server.database.models.execution import Execution as ExecutionDB
from server.platform_properties import PLATFORM_PROPERTIES
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.resources.models.pipeline import Pipeline, PipelineSchema
from server.common.error_codes_and_messages import (
    UNAUTHORIZED, INVALID_INPUT_FILE, INVALID_PATH, INVALID_MODEL_PROVIDED,
    INVALID_PIPELINE_IDENTIFIER, EXECUTION_IDENTIFIER_MUST_NOT_BE_SET,
    INVALID_QUERY_PARAMETER, INVALID_EXECUTION_TIMEOUT, PATH_DOES_NOT_EXIST,
    UNEXPECTED_ERROR, ErrorCodeAndMessageFormatter)
from server.resources.models.execution import Execution, EXECUTION_COMPLETED_STATUSES
from server.resources.helpers.pipelines import get_pipeline
from server.resources.helpers.pathnames import (
    INPUTS_FILENAME, EXECUTIONS_DIRNAME, DESCRIPTOR_FILENAME,
    CARMIN_FILES_FOLDER, STDOUT_FILENAME, STDERR_FILENAME)


def create_user_executions_dir(username: str):
    user_execution_dir = os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME)
    try:
        os.mkdir(user_execution_dir)
    except FileExistsError:
        pass
    return user_execution_dir


def create_execution_directory(execution: ExecutionDB, user: User
                               ) -> ((str, str), ErrorCodeAndMessage):

    user_execution_dir = create_user_executions_dir(user.username)
    execution_dir_absolute_path = os.path.join(user_execution_dir,
                                               execution.identifier)
    carmin_dir_absolute_path = os.path.join(execution_dir_absolute_path,
                                            CARMIN_FILES_FOLDER)

    if not is_safe_path(execution_dir_absolute_path) or not is_data_accessible(
            execution_dir_absolute_path, user):
        return (None, None), UNAUTHORIZED

    path, error = create_directory(execution_dir_absolute_path)
    carmin_path, error = create_directory(carmin_dir_absolute_path)

    return (execution_dir_absolute_path, carmin_dir_absolute_path), error


def delete_execution_directory(execution_dir_path: str):
    shutil.rmtree(execution_dir_path, ignore_errors=True)


def get_execution_dir(username: str, execution_identifier: str) -> str:
    execution_dir = os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME,
        execution_identifier)
    if not os.path.isdir(execution_dir):
        raise FileNotFoundError
    return execution_dir


def get_execution_carmin_files_dir(username: str,
                                   execution_identifier: str) -> str:
    execution_carmin_files_dir = os.path.join(
        get_execution_dir(username, execution_identifier), CARMIN_FILES_FOLDER)
    if not os.path.isdir(execution_carmin_files_dir):
        raise FileNotFoundError
    return execution_carmin_files_dir


def write_inputs_to_file(execution: Execution,
                         path_to_execution_dir: str) -> ErrorCodeAndMessage:
    inputs_json_file = os.path.join(path_to_execution_dir, INPUTS_FILENAME)
    write_content = json.dumps(execution.input_values)
    try:
        with open(inputs_json_file, 'w') as f:
            f.write(write_content)
    except OSError:
        return UNEXPECTED_ERROR


def write_absolute_path_inputs_to_file(
        username: str, execution_identifier: str,
        input_values: Dict) -> (str, ErrorCodeAndMessage):
    inputs_json_file = get_absolute_path_inputs_path(username,
                                                     execution_identifier)
    write_content = json.dumps(input_values)
    try:
        with open(inputs_json_file, 'w') as f:
            f.write(write_content)
    except OSError:
        return None, UNEXPECTED_ERROR

    return inputs_json_file, None


def get_absolute_path_inputs_path(username: str,
                                  execution_identifier: str) -> str:
    carmin_files_dir = get_execution_carmin_files_dir(username,
                                                      execution_identifier)
    absolute_path_inputs_path = os.path.join(
        carmin_files_dir, "{}.json".format(execution_identifier))
    return absolute_path_inputs_path


def input_files_exist(input_values: Dict, pipeline: Pipeline,
                      url_root: str) -> (bool, str):
    pipeline_parameters = pipeline.parameters

    for key in input_values:
        for parameter in pipeline_parameters:
            if parameter.parameter_type == "File" and not parameter.is_returned_value and parameter.identifier == key:
                exists, path = platform_path_exists(url_root,
                                                    input_values[key])
                if not exists:
                    return False, path
    return True, None


def create_absolute_path_inputs(username: str, execution_identifier: str,
                                pipeline_identifier: str,
                                url_root: str) -> (str, ErrorCodeAndMessage):
    input_values, error = load_inputs(username, execution_identifier)
    if error:
        return None, error

    pipeline = get_pipeline(pipeline_identifier)
    if not pipeline:
        return None, INVALID_PIPELINE_IDENTIFIER

    for key in input_values:
        for parameter in pipeline.parameters:
            if parameter.parameter_type == "File" and not parameter.is_returned_value and parameter.identifier == key:
                input_values[key] = path_from_data_dir(url_root,
                                                       input_values[key])

    path, error = write_absolute_path_inputs_to_file(
        username, execution_identifier, input_values)
    if error:
        return None, error
    return path, None


def load_inputs(username: str,
                execution_identifier: str) -> (Dict, ErrorCodeAndMessage):
    execution_inputs_absolute_path = get_inputs_file_path(
        username, execution_identifier)

    if not os.path.exists(execution_inputs_absolute_path):
        return None, INVALID_PATH

    with open(execution_inputs_absolute_path) as inputs_file:
        inputs = json.load(inputs_file)
        return inputs, None


def get_inputs_file_path(username: str, execution_identifier: str) -> str:
    return os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME,
        execution_identifier, CARMIN_FILES_FOLDER, INPUTS_FILENAME)


def get_execution_as_model(username: str,
                           execution_db) -> (Execution, ErrorCodeAndMessage):
    if not execution_db:
        return None, INVALID_MODEL_PROVIDED
    inputs, error = load_inputs(username, execution_db.identifier)
    if error:
        inputs = {"error": "Error retrieving inputs for execution."}
    dummy_exec = Execution()
    execution_kwargs = {
        prop: execution_db.__dict__[prop]
        for prop in dummy_exec.__dict__.keys() if prop in execution_db.__dict__
    }
    exe = Execution(input_values=inputs, **execution_kwargs)
    if exe.status in EXECUTION_COMPLETED_STATUSES:
        """This implementation does not currently respect the current
        (0.3) API specification. It simply returns a list of output files that
        were generated from the execution."""
        from server.resources.helpers.execution_results import get_output_files
        output_files = get_output_files(username, exe.identifier)
        path_list = []
        for output in output_files:
            path_list.append(output.platform_path)
        exe.returned_files = path_list
    return exe, None


def validate_request_model(model: Execution,
                           url_root: str) -> (bool, ErrorCodeAndMessage):
    if model.identifier:
        return False, EXECUTION_IDENTIFIER_MUST_NOT_BE_SET
    pipeline = get_pipeline(model.pipeline_identifier)
    if not pipeline:
        return False, INVALID_PIPELINE_IDENTIFIER
    files_exist, error = input_files_exist(model.input_values, pipeline,
                                           url_root)
    if not files_exist:
        error_code_and_message = ErrorCodeAndMessageFormatter(
            INVALID_INPUT_FILE, error)
        return False, error_code_and_message

    # Timeout validation
    min_authorized_execution_timeout = PLATFORM_PROPERTIES.get(
        "minAuthorizedExecutionTimeout", 0)
    max_authorized_execution_timeout = PLATFORM_PROPERTIES.get(
        "maxAuthorizedExecutionTimeout", 0)
    if model.timeout and ((max_authorized_execution_timeout > 0 and
                           model.timeout > max_authorized_execution_timeout) or
                          (model.timeout < min_authorized_execution_timeout)):
        error_code_and_message = ErrorCodeAndMessageFormatter(
            INVALID_EXECUTION_TIMEOUT, min_authorized_execution_timeout,
            max_authorized_execution_timeout or "(no maximum timeout)")
        return False, error_code_and_message
    return True, None


def query_converter(value):
    converted_value = int(value)
    if converted_value < 0:
        raise ValueError
    return converted_value


def copy_descriptor_to_execution_dir(execution_path,
                                     descriptor_path) -> ErrorCodeAndMessage:
    if not os.path.exists(descriptor_path):
        return PATH_DOES_NOT_EXIST

    try:
        shutil.copyfile(descriptor_path,
                        os.path.join(execution_path, DESCRIPTOR_FILENAME))
    except OSError:
        return UNEXPECTED_ERROR

    return None


def get_descriptor_path(username: str, execution_identifier: str) -> str:
    return os.path.join(
        get_execution_carmin_files_dir(username, execution_identifier),
        DESCRIPTOR_FILENAME)


def std_file_path(username: str, execution_identifier: str,
                  filename: str) -> str:
    return os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME,
        execution_identifier, CARMIN_FILES_FOLDER, filename)


def get_std_file(username: str, execution_identifier: str,
                 filename: str) -> (str, ErrorCodeAndMessage):
    file_path = std_file_path(username, execution_identifier, filename)

    try:
        with open(file_path) as f:
            return f.read(), None
    except OSError:
        return None, PATH_DOES_NOT_EXIST


def is_safe_for_get(user: User, execution_db: ExecutionDB):
    if user.role == Role.admin:
        return True
    return execution_db.creator_username == user.username


from .path import (create_directory, get_user_data_directory, is_safe_path,
                   is_data_accessible, platform_path_exists,
                   path_from_data_dir)
