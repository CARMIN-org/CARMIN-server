import os
import json
import shutil
from boutiques import bosh
from typing import Dict
from server import app
from server.database.models.user import User
from server.database.models.execution import Execution as ExecutionDB
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.resources.models.pipeline import Pipeline, PipelineSchema
from server.common.error_codes_and_messages import (
    UNAUTHORIZED, INVALID_INPUT_FILE, INVALID_PATH, INVALID_MODEL_PROVIDED,
    INVALID_PIPELINE_IDENTIFIER, EXECUTION_IDENTIFIER_MUST_NOT_BE_SET,
    INVALID_QUERY_PARAMETER, UNEXPECTED_ERROR, ErrorCodeAndMessageFormatter)
from server.resources.models.execution import Execution
from server.resources.helpers.pipelines import get_pipeline

INPUTS_FILENAME = "inputs.json"
EXECUTIONS_DIRNAME = "executions"
ABSOLUTE_PATH_INPUTS_FILENAME = "inputs_abs.json"


def create_user_executions_dir(username: str):
    user_execution_dir = os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME)
    try:
        os.mkdir(user_execution_dir)
    except FileExistsError:
        pass
    return user_execution_dir


def create_execution_directory(execution: ExecutionDB,
                               user: User) -> (str, ErrorCodeAndMessage):

    user_execution_dir = create_user_executions_dir(user.username)
    execution_dir_absolute_path = os.path.join(user_execution_dir,
                                               execution.identifier)

    if not is_safe_path(execution_dir_absolute_path) or not is_data_accessible(
            execution_dir_absolute_path, user):
        return None, UNAUTHORIZED

    path, error = create_directory(execution_dir_absolute_path)
    return execution_dir_absolute_path, error


def delete_execution_directory(execution_dir_path: str):
    shutil.rmtree(execution_dir_path, ignore_errors=True)


def get_execution_dir(username: str, execution_identifier: str) -> str:
    execution_dir = os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME,
        execution_identifier)
    if not os.path.isdir(execution_dir):
        raise FileNotFoundError
    return execution_dir


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
        input_values: Dict,
        path_to_execution_dir: str) -> (str, ErrorCodeAndMessage):
    inputs_json_file = os.path.join(path_to_execution_dir,
                                    ABSOLUTE_PATH_INPUTS_FILENAME)
    write_content = json.dumps(input_values)
    try:
        with open(inputs_json_file, 'w') as f:
            f.write(write_content)
    except OSError:
        return None, UNEXPECTED_ERROR

    return inputs_json_file, None


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

    execution_dir = get_execution_dir(username, execution_identifier)
    path, error = write_absolute_path_inputs_to_file(input_values,
                                                     execution_dir)
    if error:
        return None, error
    return path, None


def load_inputs(username: str,
                execution_identifier: str) -> (Dict, ErrorCodeAndMessage):
    execution_inputs_absolute_path = os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME,
        execution_identifier, INPUTS_FILENAME)

    if not os.path.exists(execution_inputs_absolute_path):
        return None, INVALID_PATH

    with open(execution_inputs_absolute_path) as inputs_file:
        inputs = json.load(inputs_file)
        return inputs, None


def inputs_file_path(username: str, execution_identifier: str) -> str:
    return os.path.join(
        get_user_data_directory(username), EXECUTIONS_DIRNAME,
        execution_identifier, INPUTS_FILENAME)


def get_execution_as_model(username: str,
                           execution_db) -> (Execution, ErrorCodeAndMessage):
    if not execution_db:
        return None, INVALID_MODEL_PROVIDED
    inputs, error = load_inputs(username, execution_db.identifier)
    if error:
        return None, error
    dummy_exec = Execution()
    execution_kwargs = {
        prop: execution_db.__dict__[prop]
        for prop in dummy_exec.__dict__.keys() if prop in execution_db.__dict__
    }
    exe = Execution(input_values=inputs, **execution_kwargs)
    return exe, None


def validate_request_model(model: dict,
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
    return True, None


def filter_executions(executions, offset, limit):
    if offset:
        try:
            offset = int(offset)
        except ValueError:
            return None, ErrorCodeAndMessageFormatter(INVALID_QUERY_PARAMETER,
                                                      offset, 'offset')
        if offset < 0:
            return None, ErrorCodeAndMessageFormatter(INVALID_QUERY_PARAMETER,
                                                      offset, 'offset')
        executions = executions[offset:]
    if limit:
        try:
            limit = int(limit)
        except ValueError:
            return None, ErrorCodeAndMessageFormatter(INVALID_QUERY_PARAMETER,
                                                      limit, 'limit')
        if limit < 0:
            return None, ErrorCodeAndMessageFormatter(INVALID_QUERY_PARAMETER,
                                                      limit, 'limit')
        executions = executions[0:limit]
    return executions, None


from .path import (create_directory, get_user_data_directory, is_safe_path,
                   is_data_accessible, platform_path_exists,
                   path_from_data_dir)
