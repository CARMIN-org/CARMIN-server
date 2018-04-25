import pytest
import copy
import os
import json
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session
from server.test.fakedata.users import standard_user
from server import app
from server.config import TestConfig
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.common.error_codes_and_messages import INVALID_PIPELINE_IDENTIFIER
from server.resources.models.pipeline import PipelineSchema
from server.test.fakedata.executions import execution_for_db

EXECUTION_IDENTIFIER = "test-execution-identifier"


@pytest.fixture(autouse=True)
def user_execution_folder(tmpdir_factory):
    root_directory = tmpdir_factory.mktemp('data')
    subdir = root_directory.mkdir(standard_user().username)
    user_executions = subdir.mkdir('executions')
    execution_folder = user_executions.mkdir(EXECUTION_IDENTIFIER)
    app.config['DATA_DIRECTORY'] = str(root_directory)

    return execution_folder


@pytest.fixture(autouse=True)
def data_creation(session):
    user = standard_user(encrypted=True)
    session.add(user)
    session.commit()

    execution = execution_for_db(EXECUTION_IDENTIFIER, user.username)
    session.add(execution)
    session.commit()


class TestExecutionStdOutResource():
    def test_get_execution_std_out_by_identifier(self, test_client,
                                                 user_execution_folder):
        pass
        # simple_stdout_text = "This is stdout content"
        # user_execution_folder.join("stdout.txt").write(simple_stdout_text)

        # response = test_client.get(
        #     '/executions/{}/stdout'.format(EXECUTION_IDENTIFIER),
        #     headers={
        #         "apiKey": standard_user().api_key
        #     })
        # assert response.data.decode('utf8') == simple_stdout_text
