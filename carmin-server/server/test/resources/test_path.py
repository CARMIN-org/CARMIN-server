import pytest
import os
import json
from server import app
from server.config import TestConfig
from server.test.utils import load_json_data
from server.common.error_codes_and_messages import MD5_ON_DIR, INVALID_PATH, UNAUTHORIZED
from server.resources.models.path import Path, PathSchema
from server.resources.models.error_code_and_message import (
    ErrorCodeAndMessage, ErrorCodeAndMessageSchema)
from server.resources.models.path_md5 import PathMD5, PathMD5Schema
from server.resources.path import generate_md5


@pytest.yield_fixture(scope='module')
def data_tester(tmpdir_factory):
    app.config.from_object(TestConfig)
    test_client = app.test_client()

    root_directory = tmpdir_factory.mktemp('data')
    subdir = root_directory.mkdir('subdirectory')
    subdir.join('subdir_text.txt').write(
        "this is a text file inside data/subdir")
    root_directory.join('test.txt').write("content")
    root_directory.join('file.json').write('{"test": "json"}')
    root_directory.join('directory.yml').write("-yaml file")
    app.config['DATA_DIRECTORY'] = str(root_directory)

    yield test_client


@pytest.fixture
def file_object():
    return Path(
        platform_path="file.json",
        last_modification_date=int(
            os.path.getmtime(
                os.path.join(app.config['DATA_DIRECTORY'], 'file.json'))),
        is_directory=False,
        size=16,
        mime_type='application/json')


@pytest.fixture
def dir_object():
    return Path(
        platform_path="subdirectory",
        last_modification_date=int(
            os.path.getmtime(
                os.path.join(app.config['DATA_DIRECTORY'], 'subdirectory'))),
        is_directory=True,
        size=38,
    )


class TestPathResource():
    def test_get_content_action_with_file(self, data_tester):
        response = data_tester.get('/path/file.json?action=content')
        assert response.data == b'{"test": "json"}'

    def test_get_content_action_with_invalid_file(self, data_tester):
        response = data_tester.get('/path/file2.json?action=content')
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == INVALID_PATH

    def test_get_content_action_with_dir(self, data_tester):
        response = data_tester.get('/path/subdirectory?action=content')
        assert response.headers['Content-Type'] == 'application/gzip'

    def test_get_list_action_with_dir(self, data_tester):
        requested_path = 'subdirectory'
        response = data_tester.get(
            '/path/{}?action=list'.format(requested_path))
        paths = PathSchema(many=True).load(load_json_data(response)).data
        expected_paths_list = os.listdir(
            os.path.join(app.config['DATA_DIRECTORY'], 'subdirectory'))
        for i, path in enumerate(paths):
            assert path.platform_path == os.path.join(requested_path,
                                                      expected_paths_list[i])

    def test_get_list_action_with_file_should_return_error(self, data_tester):
        response = data_tester.get('/path/file.json?action=list')
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert isinstance(error, ErrorCodeAndMessage)

    def test_get_properties_action_with_file(self, data_tester, file_object):
        response = data_tester.get('/path/file.json?action=properties')
        path = PathSchema().load(load_json_data(response)).data
        assert path == file_object

    def test_get_properties_action_with_dir(self, data_tester, dir_object):
        response = data_tester.get('/path/subdirectory?action=properties')
        path = PathSchema().load(load_json_data(response)).data
        assert path == dir_object

    def test_query_outside_data_returns_error(self, data_tester):
        response = data_tester.get('/path/../../.?action=properties')
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == UNAUTHORIZED

    def test_get_md5_action_with_file(self, data_tester):
        response = data_tester.get('/path/file.json?action=md5')
        md5 = PathMD5Schema().load(load_json_data(response)).data
        assert md5.md5 == generate_md5(
            os.path.join(app.config['DATA_DIRECTORY'], "file.json"))

    def test_get_md5_action_with_dir_should_return_error(self, data_tester):
        response = data_tester.get('/path/subdirectory?action=md5')
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == MD5_ON_DIR
