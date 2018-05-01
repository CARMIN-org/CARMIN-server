import copy
import os
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk
import json
import pytest
from server import app
from server.common.error_codes_and_messages import (
    EXECUTION_IDENTIFIER_MUST_NOT_BE_SET, INVALID_PIPELINE_IDENTIFIER,
    INVALID_MODEL_PROVIDED, INVALID_INPUT_FILE, INVALID_QUERY_PARAMETER)
from server.resources.models.pipeline import PipelineSchema
from server.resources.models.execution import ExecutionSchema
from server.test.fakedata.pipelines import PipelineStub, BOUTIQUES_SLEEP_ORIGINAL, BOUTIQUES_SLEEP_CONVERTED
from server.test.fakedata.executions import (
    post_valid_execution, post_invalid_execution_file_not_exist,
    post_invalid_execution_array_file_not_exist, post_invalid_identifier_set,
    POST_INVALID_EXECUTION_IDENTIFIER_NOT_EXIST, POST_INVALID_MODEL)
from server.test.fakedata.users import standard_user
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session
from server.resources.helpers.executions import INPUTS_FILENAME, DESCRIPTOR_FILENAME


@pytest.fixture
def pipeline():
    return PipelineStub(BOUTIQUES_SLEEP_ORIGINAL, BOUTIQUES_SLEEP_CONVERTED,
                        "sleep.json")


@pytest.fixture(autouse=True)
def test_config(tmpdir_factory, session, pipeline):
    session.add(standard_user(encrypted=True))
    session.commit()

    pipelines_root = tmpdir_factory.mktemp('pipelines')
    pipelines_root.join(pipeline.get_converted_filename()).write(
        pipeline.get_converted_json())
    boutiques_dir = pipelines_root.mkdir(pipeline.descriptor_type)
    boutiques_dir.join(pipeline.get_original_filename()).write(
        pipeline.get_original_json())
    app.config['PIPELINE_DIRECTORY'] = str(pipelines_root)

    data_root = tmpdir_factory.mktemp('data')
    user_dir = data_root.mkdir(standard_user().username)
    user_dir.join('test.txt').write('test file')
    user_execution_dir = user_dir.mkdir('executions')
    app.config['DATA_DIRECTORY'] = str(data_root)


@pytest.fixture
def number_of_executions(test_client, pipeline) -> int:
    number_of_executions = 10
    for _ in range(number_of_executions):
        test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                post_valid_execution(pipeline.identifier)).data))
    return number_of_executions


class TestExecutionsResource():
    # tests for POST
    def test_post_valid_execution(self, test_client, pipeline):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                post_valid_execution(pipeline.identifier)).data))
        assert response.status_code == 200

        json_response = load_json_data(response)
        execution = ExecutionSchema().load(json_response).data
        execution_dir = os.path.join(user_execution_dir, execution.identifier)
        carmin_files_dir = os.path.join(execution_dir, ".carmin-files")
        assert os.path.isdir(execution_dir)
        assert os.path.isdir(carmin_files_dir)
        assert INPUTS_FILENAME in os.listdir(carmin_files_dir)
        assert DESCRIPTOR_FILENAME in os.listdir(carmin_files_dir)

    def test_post_file_doesnt_exist(self, test_client, pipeline):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                post_invalid_execution_file_not_exist(
                    pipeline.identifier)).data))
        assert not os.listdir(user_execution_dir)
        assert response.status_code == 400

    def test_post_array_file_doesnt_exist(self, test_client, pipeline):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        execution = post_invalid_execution_array_file_not_exist(
            pipeline.identifier)
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(execution).data))
        error_code_and_message = error_from_response(response)

        expected_error_code_and_message = copy.deepcopy(INVALID_INPUT_FILE)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            *execution.input_values["input_file"])
        assert not os.listdir(user_execution_dir)
        assert error_code_and_message == expected_error_code_and_message

    def test_post_identifier_set(self, test_client, pipeline):
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                post_invalid_identifier_set(pipeline.identifier)).data))
        error = error_from_response(response)
        assert error == EXECUTION_IDENTIFIER_MUST_NOT_BE_SET

    def test_post_pipeline_identifier_doesnt_exist(self, test_client):
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                POST_INVALID_EXECUTION_IDENTIFIER_NOT_EXIST).data))
        error = error_from_response(response)
        assert error == INVALID_PIPELINE_IDENTIFIER

    def test_post_invalid_model(self, test_client):
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=POST_INVALID_MODEL)
        error = error_from_response(response)
        assert error == INVALID_MODEL_PROVIDED

    def test_get_without_executions(self, test_client):
        response = test_client.get(
            '/executions', headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        executions = ExecutionSchema(many=True).load(json_response).data
        assert not executions

    def test_get_with_executions(self, test_client, number_of_executions):
        response = test_client.get(
            '/executions', headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        executions, error = ExecutionSchema(many=True).load(json_response)
        assert not error
        assert len(executions) == number_of_executions

    def test_get_with_offset(self, test_client, number_of_executions):
        offset = 6
        response = test_client.get(
            '/executions?offset={}'.format(offset),
            headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        assert len(json_response) == number_of_executions - offset

    def test_get_with_invalid_offset(self, test_client, number_of_executions):
        offset = "invalid"
        response = test_client.get(
            '/executions?offset={}'.format(offset),
            headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        assert len(json_response) == number_of_executions

    def test_get_with_offset_greater_than_execution_count(
            self, test_client, number_of_executions):
        offset = 1000
        response = test_client.get(
            '/executions?offset={}'.format(offset),
            headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        assert len(json_response) == 0

    def test_get_with_negative_offset(self, test_client, number_of_executions):
        offset = -10
        response = test_client.get(
            '/executions?offset={}'.format(offset),
            headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        assert len(json_response) == number_of_executions

    def test_get_with_limit(self, test_client, number_of_executions):
        limit = 4
        response = test_client.get(
            '/executions?limit={}'.format(limit),
            headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        assert len(json_response) == limit

    def test_get_with_invalid_limit(self, test_client, number_of_executions):
        limit = "invalid"
        response = test_client.get(
            '/executions?limit={}'.format(limit),
            headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        assert len(json_response) == number_of_executions

    def test_get_with_negative_limit(self, test_client, number_of_executions):
        limit = -10
        response = test_client.get(
            '/executions?limit={}'.format(limit),
            headers={
                "apiKey": standard_user().api_key
            })
        json_response = load_json_data(response)
        assert len(json_response) == number_of_executions
