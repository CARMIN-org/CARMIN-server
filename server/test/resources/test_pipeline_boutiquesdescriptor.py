import pytest
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
from server.test.fakedata.pipelines import (NameStudyOne, PipelineOne)


@pytest.fixture(autouse=True)
def data_tester(tmpdir_factory):
    root_directory = tmpdir_factory.mktemp('pipelines')

    root_directory.join("boutiques_pipeline1.json").write(
        PipelineSchema().dumps(PipelineOne).data)

    boutiques_directory = root_directory.mkdir('boutiques')

    boutiques_directory.join('pipeline1.json').write(
        PipelineSchema().dumps(PipelineOne).data)

    app.config['PIPELINE_DIRECTORY'] = str(root_directory)


@pytest.fixture(autouse=True)
def user_creator(session):
    session.add(standard_user(encrypted=True))
    session.commit()


class TestPipelineBoutiquesDescriptorResource():
    def test_get_pipeline_boutiques_descriptor_by_identifier(
            self, test_client):
        response = test_client.get(
            '/pipelines/{}/boutiquesdescriptor'.format(PipelineOne.identifier),
            headers={"apiKey": standard_user().api_key})
        pipeline = load_json_data(response)
        original_pipeline = json.loads(
            PipelineSchema().dumps(PipelineOne).data)

        assert pipeline == original_pipeline

    def test_get_pipeline_boutiques_descriptor_by_identifier_invalid_id(
            self, test_client):
        response = test_client.get(
            '/pipelines/{}/boutiquesdescriptor'.format("INVALID_{}".format(
                PipelineOne.identifier)),
            headers={"apiKey": standard_user().api_key})
        error = error_from_response(response)
        assert error == INVALID_PIPELINE_IDENTIFIER
