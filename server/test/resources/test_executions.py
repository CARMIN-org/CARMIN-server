import copy
import os
import json
import pytest
from server import app
from server.common.error_codes_and_messages import (
    EXECUTION_IDENTIFIER_MUST_NOT_BE_SET, INVALID_PIPELINE_IDENTIFIER,
    INVALID_MODEL_PROVIDED, INVALID_INPUT_FILE, INVALID_QUERY_PARAMETER)
from server.resources.models.pipeline import PipelineSchema
from server.resources.models.execution import ExecutionSchema
from server.test.fakedata.pipelines import PIPELINE_FOUR
from server.test.fakedata.executions import (
    POST_VALID_EXECUTION, POST_INVALID_EXECUTION_FILE_NOT_EXIST,
    POST_INVALID_EXECUTION_ARRAY_FILE_NOT_EXIST, POST_INVALID_IDENTIFIER_SET,
    POST_INVALID_EXECUTION_IDENTIFIER_NOT_EXIST, POST_INVALID_MODEL)
from server.test.fakedata.users import standard_user
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session


@pytest.fixture(autouse=True)
def test_config(tmpdir_factory, session):
    session.add(standard_user(encrypted=True))
    session.commit()

    pipelines_root = tmpdir_factory.mktemp('pipelines')
    data_root = tmpdir_factory.mktemp('data')
    pipelines_root.join('pipeline1.json').write(
        json.dumps(PipelineSchema().dump(PIPELINE_FOUR).data))
    user_dir = data_root.mkdir(standard_user().username)
    user_dir.join('test.txt').write('test file')
    user_execution_dir = user_dir.mkdir('executions')
    app.config['DATA_DIRECTORY'] = str(data_root)
    app.config['PIPELINE_DIRECTORY'] = str(pipelines_root)


@pytest.fixture
def number_of_executions(test_client) -> int:
    number_of_executions = 10
    for _ in range(number_of_executions):
        test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(POST_VALID_EXECUTION).data))
    return number_of_executions


class TestExecutionsResource():
    # tests for POST
    def test_post_valid_execution(self, test_client):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(POST_VALID_EXECUTION).data))
        assert os.listdir(user_execution_dir)
        assert response.status_code == 200

    def test_post_file_doesnt_exist(self, test_client):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                POST_INVALID_EXECUTION_FILE_NOT_EXIST).data))
        assert not os.listdir(user_execution_dir)
        assert response.status_code == 400

    def test_post_array_file_doesnt_exist(self, test_client):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                POST_INVALID_EXECUTION_ARRAY_FILE_NOT_EXIST).data))
        error_code_and_message = error_from_response(response)

        expected_error_code_and_message = copy.deepcopy(INVALID_INPUT_FILE)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            *POST_INVALID_EXECUTION_ARRAY_FILE_NOT_EXIST.
            input_values["file_input"])
        assert not os.listdir(user_execution_dir)
        assert error_code_and_message == expected_error_code_and_message

    def test_post_identifier_set(self, test_client):
        response = test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(
                ExecutionSchema().dump(POST_INVALID_IDENTIFIER_SET).data))
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
        error = error_from_response(response)

        expected_error_code_and_message = copy.deepcopy(
            INVALID_QUERY_PARAMETER)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            offset, 'offset')
        assert error == expected_error_code_and_message

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
        error = error_from_response(response)

        expected_error_code_and_message = copy.deepcopy(
            INVALID_QUERY_PARAMETER)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            offset, 'offset')
        assert error == expected_error_code_and_message

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
        error = error_from_response(response)

        expected_error_code_and_message = copy.deepcopy(
            INVALID_QUERY_PARAMETER)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            limit, 'limit')
        assert error == expected_error_code_and_message

    def test_get_with_negative_limit(self, test_client, number_of_executions):
        limit = -10
        response = test_client.get(
            '/executions?limit={}'.format(limit),
            headers={
                "apiKey": standard_user().api_key
            })

        error = error_from_response(response)

        expected_error_code_and_message = copy.deepcopy(
            INVALID_QUERY_PARAMETER)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            limit, 'limit')
        assert error == expected_error_code_and_message
