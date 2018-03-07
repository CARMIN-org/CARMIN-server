import pytest
import os
import json
from server import app
from server.common.error_codes_and_messages import (
    EXECUTION_IDENTIFIER_MUST_NOT_BE_SET, INVALID_PIPELINE_IDENTIFIER,
    INVALID_MODEL_PROVIDED, INVALID_INPUT_FILE)
from server.resources.models.pipeline import PipelineSchema
from server.resources.models.execution import ExecutionSchema
from server.test.fakedata.pipelines import PIPELINE_FOUR
from server.test.fakedata.executions import (
    POST_VALID_EXECUTION, POST_INVALID_EXECUTION_FILE_NOT_EXIST,
    POST_INVALID_EXECUTION_ARRAY_FILE_NOT_EXIST, POST_INVALID_IDENTIFIER_SET,
    POST_INVALID_EXECUTION_IDENTIFIER_NOT_EXIST, POST_INVALID_MODEL)
from server.test.fakedata.users import standard_user
from server.test.utils import get_test_config, error_from_response


@pytest.yield_fixture()
def test_config(tmpdir_factory):
    test_config = get_test_config()
    test_config.db.session.add(standard_user(encrypted=True))
    test_config.db.session.commit()

    pipelines_root = tmpdir_factory.mktemp('pipelines')
    data_root = tmpdir_factory.mktemp('data')
    pipelines_root.join('pipeline1.json').write(
        json.dumps(PipelineSchema().dump(PIPELINE_FOUR).data))
    user_dir = data_root.mkdir(standard_user().username)
    user_dir.join('test.txt').write('test file')
    user_execution_dir = user_dir.mkdir('executions')
    app.config['DATA_DIRECTORY'] = str(data_root)
    app.config['PIPELINE_DIRECTORY'] = str(pipelines_root)

    yield test_config

    test_config.db.drop_all()


class TestExecutionsResource():
    # tests for POST
    def test_post_valid_execution(self, test_config):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_config.test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(POST_VALID_EXECUTION).data))
        assert os.listdir(user_execution_dir)
        assert response.status_code == 200

    def test_post_file_doesnt_exist(self, test_config):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_config.test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                POST_INVALID_EXECUTION_FILE_NOT_EXIST).data))
        assert not os.listdir(user_execution_dir)
        assert response.status_code == 400

    def test_post_array_file_doesnt_exist(self, test_config):
        user_execution_dir = os.path.join(app.config['DATA_DIRECTORY'],
                                          standard_user().username,
                                          'executions')
        response = test_config.test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                POST_INVALID_EXECUTION_ARRAY_FILE_NOT_EXIST).data))
        error_code_and_message = error_from_response(response)

        assert not os.listdir(user_execution_dir)
        assert error_code_and_message == INVALID_INPUT_FILE

    def test_post_identifier_set(self, test_config):
        response = test_config.test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(
                ExecutionSchema().dump(POST_INVALID_IDENTIFIER_SET).data))
        error = error_from_response(response)
        assert error == EXECUTION_IDENTIFIER_MUST_NOT_BE_SET

    def test_post_pipeline_identifier_doesnt_exist(self, test_config):
        response = test_config.test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(ExecutionSchema().dump(
                POST_INVALID_EXECUTION_IDENTIFIER_NOT_EXIST).data))
        error = error_from_response(response)
        assert error == INVALID_PIPELINE_IDENTIFIER

    def test_post_invalid_model(self, test_config):
        response = test_config.test_client.post(
            '/executions',
            headers={"apiKey": standard_user().api_key},
            data=POST_INVALID_MODEL)
        error = error_from_response(response)
        assert error == INVALID_MODEL_PROVIDED
