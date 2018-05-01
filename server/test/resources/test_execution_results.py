import json
import copy
import os
import pytest
from server import app
from server.resources.models.path import PathSchema
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, EXECUTION_NOT_FOUND,
    CANNOT_GET_RESULT_NOT_COMPLETED_EXECUTION, UNAUTHORIZED)
from server.database.models.execution import ExecutionStatus
from server.test.fakedata.users import standard_user, standard_user_2
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session
from server.resources.models.execution import ExecutionSchema
from server.test.fakedata.executions import post_valid_execution
from server.test.fakedata.pipelines import (
    PipelineStub, BOUTIQUES_NO_SLEEP_ORIGINAL, BOUTIQUES_NO_SLEEP_CONVERTED)


@pytest.fixture
def pipeline_no_sleep():
    return PipelineStub(BOUTIQUES_NO_SLEEP_ORIGINAL,
                        BOUTIQUES_NO_SLEEP_CONVERTED, "no_sleep.json")


@pytest.fixture
def post_execution_no_sleep(test_client, pipeline_no_sleep):
    execution_no_sleep = post_valid_execution(pipeline_no_sleep.identifier)
    response = test_client.post(
        '/executions',
        headers={"apiKey": standard_user().api_key},
        data=json.dumps(ExecutionSchema().dump(execution_no_sleep).data))
    json_response = load_json_data(response)
    return ExecutionSchema().load(json_response).data.identifier


@pytest.fixture
def test_config(tmpdir_factory, session, test_client, pipeline_no_sleep):
    session.add(standard_user(encrypted=True))
    session.add(standard_user_2(encrypted=True))
    session.commit()

    pipelines_root = tmpdir_factory.mktemp('pipelines')
    pipelines_root.join(pipeline_no_sleep.get_converted_filename()).write(
        pipeline_no_sleep.get_converted_json())

    boutiques_dir = pipelines_root.mkdir('boutiques')
    boutiques_dir.join(pipeline_no_sleep.get_original_filename()).write(
        pipeline_no_sleep.get_original_json())
    app.config['PIPELINE_DIRECTORY'] = str(pipelines_root)

    data_root = tmpdir_factory.mktemp('data')
    user_dir = data_root.mkdir(standard_user().username)
    user_dir.join('test.txt').write('Jane Doe')
    user_execution_dir = user_dir.mkdir('executions')
    app.config['DATA_DIRECTORY'] = str(data_root)


@pytest.fixture
def play_execution_no_sleep(test_client, post_execution_no_sleep):
    response = test_client.get(
        '/executions', headers={"apiKey": standard_user().api_key})
    response = test_client.put(
        '/executions/{}/play'.format(post_execution_no_sleep),
        headers={
            "apiKey": standard_user().api_key,
        })
    assert response.status_code == 204


class TestExecutionResults():
    def test_get_results_invalid_execution_id(self, test_client, test_config,
                                              post_execution_no_sleep):
        invalid_id = "NOT_{}".format(post_execution_no_sleep)
        response = test_client.get(
            '/executions/{}/results'.format(invalid_id),
            headers={"apiKey": standard_user().api_key})
        error = error_from_response(response)
        expected_error_code_and_message = ErrorCodeAndMessageFormatter(
            EXECUTION_NOT_FOUND, invalid_id)
        assert error == expected_error_code_and_message

    def test_get_results_not_completed_execution(
            self, test_client, test_config, post_execution_no_sleep):
        response = test_client.get(
            '/executions/{}/results'.format(post_execution_no_sleep),
            headers={"apiKey": standard_user().api_key})
        error = error_from_response(response)
        expected_error_code_and_message = ErrorCodeAndMessageFormatter(
            CANNOT_GET_RESULT_NOT_COMPLETED_EXECUTION,
            ExecutionStatus.Initializing.name)
        assert error == expected_error_code_and_message

    def test_get_results_user_not_owner(self, test_client, test_config,
                                        post_execution_no_sleep):
        response = test_client.get(
            '/executions/{}/results'.format(post_execution_no_sleep),
            headers={"apiKey": standard_user_2().api_key})
        error = error_from_response(response)
        assert error == UNAUTHORIZED

    def test_get_results_success(self, test_client, test_config,
                                 post_execution_no_sleep,
                                 play_execution_no_sleep):
        response = test_client.get(
            '/executions/{}/results'.format(post_execution_no_sleep),
            headers={"apiKey": standard_user().api_key})
        assert response.status_code == 200
        paths = PathSchema(many=True).load(load_json_data(response)).data
        assert len(paths) == 1
        output_file_path = os.path.relpath(
            os.path.join(app.config['DATA_DIRECTORY'],
                         standard_user().username, "executions",
                         post_execution_no_sleep, BOUTIQUES_NO_SLEEP_ORIGINAL[
                             "output-files"][0]["path-template"]),
            app.config['DATA_DIRECTORY'])
        relative_returned_path = paths[0].platform_path.split("/path/", 1)[1]
        assert relative_returned_path == output_file_path
