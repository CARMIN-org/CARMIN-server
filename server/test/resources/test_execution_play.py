import json
import copy
import os
import pytest
from server import app
from server.test.fakedata.users import standard_user
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session
from server.resources.models.execution import ExecutionSchema
from server.test.fakedata.executions import post_valid_execution
from server.test.fakedata.pipelines import (
    PipelineStub, BOUTIQUES_SLEEP_ORIGINAL, BOUTIQUES_SLEEP_CONVERTED,
    BOUTIQUES_NO_SLEEP_ORIGINAL, BOUTIQUES_NO_SLEEP_CONVERTED)


@pytest.fixture
def pipeline_sleep():
    return PipelineStub(BOUTIQUES_SLEEP_ORIGINAL, BOUTIQUES_SLEEP_CONVERTED,
                        "sleep.json")


@pytest.fixture
def pipeline_no_sleep():
    return PipelineStub(BOUTIQUES_NO_SLEEP_ORIGINAL,
                        BOUTIQUES_NO_SLEEP_CONVERTED, "no_sleep.json")


@pytest.fixture
def post_execution_sleep(test_client, pipeline_sleep):
    execution_sleep = post_valid_execution(pipeline_sleep.identifier)
    response = test_client.post(
        '/executions',
        headers={"apiKey": standard_user().api_key},
        data=json.dumps(ExecutionSchema().dump(execution_sleep).data))
    json_response = load_json_data(response)
    return ExecutionSchema().load(json_response).data.identifier


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
def test_config(tmpdir_factory, session, test_client, pipeline_sleep,
                pipeline_no_sleep):
    session.add(standard_user(encrypted=True))
    session.commit()

    pipelines_root = tmpdir_factory.mktemp('pipelines')
    pipelines_root.join(pipeline_sleep.get_converted_filename()).write(
        pipeline_sleep.get_converted_json())
    pipelines_root.join(pipeline_no_sleep.get_converted_filename()).write(
        pipeline_no_sleep.get_converted_json())

    boutiques_dir = pipelines_root.mkdir('boutiques')
    boutiques_dir.join(pipeline_sleep.get_original_filename()).write(
        pipeline_sleep.get_original_json())
    boutiques_dir.join(pipeline_no_sleep.get_original_filename()).write(
        pipeline_no_sleep.get_original_json())
    app.config['PIPELINE_DIRECTORY'] = str(pipelines_root)

    data_root = tmpdir_factory.mktemp('data')
    user_dir = data_root.mkdir(standard_user().username)
    user_dir.join('test.txt').write('Jane Doe')
    user_execution_dir = user_dir.mkdir('executions')
    app.config['DATA_DIRECTORY'] = str(data_root)


class TestExecutionPlayResource():
    def test_put_execution_play_fast(self, test_client, test_config,
                                     post_execution_no_sleep):
        response = test_client.get(
            '/executions', headers={"apiKey": standard_user().api_key})
        response = test_client.put(
            '/executions/{}/play'.format(post_execution_no_sleep),
            headers={
                "apiKey": standard_user().api_key,
            })
        assert response.status_code == 204

        output_path = os.path.join(app.config['DATA_DIRECTORY'],
                                   standard_user().username, 'executions',
                                   post_execution_no_sleep, 'greeting.txt')
        assert os.path.exists(output_path)

        with open(output_path) as f:
            assert f.read() == 'Welcome to CARMIN-Server, Jane Doe.\n'
