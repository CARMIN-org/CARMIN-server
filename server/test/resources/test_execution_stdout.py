import pytest
import os
import json
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session
from server.test.fakedata.users import standard_user
from server.test.fakedata.executions import post_valid_execution
from server.test.fakedata.pipelines import PipelineStub, BOUTIQUES_SLEEP_ORIGINAL, BOUTIQUES_SLEEP_CONVERTED
from server import app
from server.config import TestConfig
from server.resources.models.execution import ExecutionSchema
from server.resources.helpers.executions import get_execution_carmin_files_dir
from server.common.error_codes_and_messages import ErrorCodeAndMessageFormatter, EXECUTION_NOT_FOUND, PATH_DOES_NOT_EXIST


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


@pytest.fixture
def write_std_out(execution_id) -> str:
    carmin_dir = get_execution_carmin_files_dir(standard_user().username,
                                                execution_id)
    simple_stdout_text = "This is stdout content"
    with open(os.path.join(carmin_dir, "stdout.txt"), "w") as f:
        f.write(simple_stdout_text)

    return simple_stdout_text


class TestExecutionStdOutResource():
    def test_get_execution_std_out_by_identifier(self, test_client,
                                                 execution_id, write_std_out):
        response = test_client.get(
            '/executions/{}/stdout'.format(execution_id),
            headers={"apiKey": standard_user().api_key})
        assert response.data.decode('utf8') == write_std_out

    def test_get_execution_std_out_not_found(self, test_client, execution_id):
        response = test_client.get(
            '/executions/{}/stdout'.format(execution_id),
            headers={"apiKey": standard_user().api_key})
        error = error_from_response(response)
        assert error == PATH_DOES_NOT_EXIST

    def test_get_execution_std_out_invalid_execution_id(
            self, test_client, execution_id, write_std_out):
        invalid_execution_id = "NOT_{}".format(execution_id)
        response = test_client.get(
            '/executions/{}/stdout'.format(invalid_execution_id),
            headers={"apiKey": standard_user().api_key})
        error = error_from_response(response)
        expected_error_code_and_message = ErrorCodeAndMessageFormatter(
            EXECUTION_NOT_FOUND, invalid_execution_id)
        assert error == expected_error_code_and_message
