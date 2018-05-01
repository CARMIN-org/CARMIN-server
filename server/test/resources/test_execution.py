import json
import copy
import pytest

from server import app
from server.database.models.execution import Execution as ExecutionDB
from server.resources.helpers.executions import get_execution_as_model
from server.resources.models.execution import ExecutionSchema, Execution
from server.common.error_codes_and_messages import EXECUTION_NOT_FOUND, ErrorCodeAndMessageFormatter
from server.test.fakedata.executions import (
    post_valid_execution, PATCH_VALID_EXECUTION, PATCH_ILLEGAL_PARAMETER,
    PATCH_ILLEGAL_PARAMETER2, PATCH_VALID_EXECUTION2, PATCH_VALID_EXECUTION3,
    PATCH_INVALID_PARAMETER, PATCH_NO_CHANGE_PARAMETER)
from server.test.fakedata.pipelines import PipelineStub, BOUTIQUES_SLEEP_ORIGINAL, BOUTIQUES_SLEEP_CONVERTED
from server.test.fakedata.users import standard_user
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session


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
def execution_id(test_client, pipeline) -> str:
    response = test_client.post(
        '/executions',
        headers={"apiKey": standard_user().api_key},
        data=json.dumps(ExecutionSchema().dump(
            post_valid_execution(pipeline.identifier)).data))
    json_response = load_json_data(response)
    return ExecutionSchema().load(json_response).data.identifier


class TestExecutionResource():
    def test_get_execution(self, test_client, execution_id):
        response = test_client.get(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key})
        json_response = load_json_data(response)
        execution = ExecutionSchema().load(json_response).data
        assert isinstance(execution, Execution)

    def test_get_invalid_execution(self, test_client):
        execution_id = "invalid"
        response = test_client.get(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key})
        error = error_from_response(response)
        expected_error_code_and_message = ErrorCodeAndMessageFormatter(
            EXECUTION_NOT_FOUND, execution_id)
        assert error == expected_error_code_and_message

    def test_put_valid_execution_name_and_timeout(self, test_client, session,
                                                  execution_id):
        response = test_client.put(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(PATCH_VALID_EXECUTION))
        assert response.status_code == 204

        execution = session.query(ExecutionDB).filter_by(
            identifier=execution_id).first()
        execution, _ = get_execution_as_model(standard_user().username,
                                              execution)
        assert execution.name == PATCH_VALID_EXECUTION["name"]
        assert execution.timeout == PATCH_VALID_EXECUTION["timeout"]

    def test_put_valid_execution_name(self, test_client, session,
                                      execution_id):
        response = test_client.put(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(PATCH_VALID_EXECUTION2))
        assert response.status_code == 204

        execution = session.query(ExecutionDB).filter_by(
            identifier=execution_id).first()
        execution, _ = get_execution_as_model(standard_user().username,
                                              execution)
        assert execution.name == PATCH_VALID_EXECUTION2["name"]

    def test_put_valid_execution_timeout(self, test_client, session,
                                         execution_id):
        response = test_client.put(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(PATCH_VALID_EXECUTION3))
        assert response.status_code == 204

        execution = session.query(ExecutionDB).filter_by(
            identifier=execution_id).first()
        execution, _ = get_execution_as_model(standard_user().username,
                                              execution)
        assert execution.timeout == PATCH_VALID_EXECUTION3["timeout"]

    def test_put_illegal_parameter_status(self, test_client, execution_id):
        response = test_client.put(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(PATCH_ILLEGAL_PARAMETER))
        error = error_from_response(response)
        expected_error_code_and_message = copy.deepcopy(error)
        expected_error_code_and_message.error_message = error.error_message.format(
            "status")
        assert error == expected_error_code_and_message

    def test_put_illegal_parameter_identifier(self, test_client, execution_id):
        response = test_client.put(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(PATCH_ILLEGAL_PARAMETER2))
        error = error_from_response(response)
        expected_error_code_and_message = copy.deepcopy(error)
        expected_error_code_and_message.error_message = error.error_message.format(
            "identifier")
        assert error == expected_error_code_and_message

    def test_put_invalid_parameter(self, test_client, execution_id):
        response = test_client.put(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(PATCH_INVALID_PARAMETER))
        assert response.status_code == 400

    def test_put_parameter_no_change(self, test_client, session, execution_id):
        response = test_client.put(
            '/executions/{}'.format(execution_id),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(PATCH_NO_CHANGE_PARAMETER))
        assert response.status_code == 204

        execution = session.query(ExecutionDB).filter_by(
            identifier=execution_id).first()
        execution, _ = get_execution_as_model(standard_user().username,
                                              execution)
        assert (execution.pipeline_identifier !=
                PATCH_NO_CHANGE_PARAMETER["pipelineIdentifier"])
