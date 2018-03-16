import pytest
import os
import json
from server.test.utils import load_json_data
from server.test.conftest import test_client
from server import app
from server.config import TestConfig
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.common.error_codes_and_messages import MISSING_PIPELINE_PROPERTY
from server.resources.models.pipeline import PipelineSchema
from server.test.fakedata.pipelines import (
    NameStudyOne, NameStudyTwo, PipelineOne, PipelineTwo, PipelineThree,
    PropNameOne, PropNameTwo, PropValueOne, PropValueTwo, PropValueThree)


@pytest.fixture(scope='module', autouse=True)
def data_tester(tmpdir_factory):
    root_directory = tmpdir_factory.mktemp('pipelines', numbered=False)

    study_one_directory = root_directory.mkdir(NameStudyOne)

    study_one_directory.join('pipeline1.json').write(
        PipelineSchema().dumps(PipelineOne).data)

    study_one_directory.join('pipeline2.json').write(
        PipelineSchema().dumps(PipelineTwo).data)

    study_two_directory = root_directory.mkdir(NameStudyTwo)
    study_two_directory.join('pipeline3.json').write(
        PipelineSchema().dumps(PipelineThree).data)

    app.config['PIPELINE_DIRECTORY'] = str(root_directory)


class TestPipelinesResource():
    def test_get_pipeline_by_identifier(self, test_client):
        response = test_client.get('/pipelines/{}'.format(
            PipelineOne.identifier))
        pipeline = PipelineSchema().load(load_json_data(response)).data
        assert pipeline == PipelineOne

    def test_get_pipeline_by_identifier_no_result(self, test_client):
        response = test_client.get('/pipelines/{}'.format(
            "NOT_{}".format(PipelineOne.identifier)))
        pipeline = PipelineSchema().load(load_json_data(response)).data
        assert not pipeline

    def test_get_content_action_empty(self, test_client):
        response = test_client.get('/pipelines')
        pipeline = PipelineSchema(many=True).load(
            load_json_data(response)).data
        assert PipelineOne in pipeline
        assert PipelineTwo in pipeline
        assert PipelineThree in pipeline

    def test_get_content_action_with_study_identifier(self, test_client):
        response = test_client.get(
            '/pipelines?studyIdentifier={}'.format(NameStudyOne))
        pipeline = PipelineSchema(many=True).load(
            load_json_data(response)).data
        assert PipelineOne in pipeline
        assert PipelineTwo in pipeline
        assert PipelineThree not in pipeline

    def test_get_content_action_with_property(self, test_client):
        response = test_client.get(
            '/pipelines?property={}'.format(PropNameOne))
        pipeline = PipelineSchema(many=True).load(
            load_json_data(response)).data
        assert PipelineOne in pipeline
        assert PipelineTwo not in pipeline
        assert PipelineThree in pipeline

    def test_get_content_action_with_only_property_value(self, test_client):
        response = test_client.get(
            '/pipelines?propertyValue={}'.format(PropValueOne))
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == MISSING_PIPELINE_PROPERTY

    def test_get_content_action_with_property_name_and_property_value(
            self, test_client):
        response = test_client.get(
            '/pipelines?property={}&propertyValue={}'.format(
                PropNameOne, PropValueOne))
        pipeline = PipelineSchema(many=True).load(
            load_json_data(response)).data
        assert PipelineOne in pipeline
        assert PipelineTwo not in pipeline
        assert PipelineThree not in pipeline
