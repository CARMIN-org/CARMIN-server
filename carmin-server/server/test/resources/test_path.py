import pytest
import os
import json
import zipfile
from server import app
from server.config import TestConfig
from server.test.utils import load_json_data
from server.test.utils import error_from_response
from server.common.error_codes_and_messages import (
    MD5_ON_DIR, INVALID_PATH, UNAUTHORIZED, ACTION_REQUIRED, INVALID_ACTION,
    LIST_ACTION_ON_FILE, INVALID_UPLOAD_TYPE)
from server.resources.models.path import Path, PathSchema
from server.resources.models.error_code_and_message import (
    ErrorCodeAndMessage, ErrorCodeAndMessageSchema)
from server.resources.models.path_md5 import PathMD5, PathMD5Schema
from server.resources.models.upload_data import UploadData, UploadDataSchema
from server.resources.models.boolean_response import BooleanResponseSchema
from server.resources.path import generate_md5


@pytest.yield_fixture()
def data_tester(tmpdir_factory):
    app.config.from_object(TestConfig)
    test_client = app.test_client()

    root_directory = tmpdir_factory.mktemp('data')
    root_directory.mkdir('empty_dir')
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
        platform_path="http://localhost/path/file.json",
        last_modification_date=int(
            os.path.getmtime(
                os.path.join(app.config['DATA_DIRECTORY'], 'file.json'))),
        is_directory=False,
        size=16,
        mime_type='application/json')


@pytest.fixture
def dir_object():
    return Path(
        platform_path="http://localhost/path/subdirectory",
        last_modification_date=int(
            os.path.getmtime(
                os.path.join(app.config['DATA_DIRECTORY'], 'subdirectory'))),
        is_directory=True,
        size=38,
    )


@pytest.fixture
def put_file():
    return UploadData(
        base64_content="VGhpcyBpcyBhIHRlc3QgZmlsZSE=",
        upload_type="File",
        md5="5dcd075938007ceb7164df6e0b21032f")


@pytest.fixture
def put_dir():
    base64 = "UEsDBAoAAAAAAH2ORUwAAAAAAAAAAAAAAAALABAAZXhlY3V0aW9ucy9VWAwAjviBWg7geFr1ARQAUEsBAhUDCgAAAAAAfY5FTAAAAAAAAAAAAAAAAAsADAAAAAAAAAAAQO1BAAAAAGV4ZWN1dGlvbnMvVVgIAI74gVoO4HhaUEsFBgAAAAABAAEARQAAADkAAAAAAA=="
    return UploadData(base64_content=base64, upload_type="Archive", md5='')


class TestPathResource():

    # tests for GET

    def test_query_outside_authorized_directory(self, data_tester):
        response = data_tester.get('/path/../../test?action=properties')
        error = error_from_response(response)
        assert error == UNAUTHORIZED

    def test_get_no_action(self, data_tester):
        response = data_tester.get('/path/file.json')
        error = error_from_response(response)
        assert error == ACTION_REQUIRED

    def test_get_invalid_action(self, data_tester):
        response = data_tester.get('/path/file.json?action=invalid')
        error = error_from_response(response)
        assert error == INVALID_ACTION

    def test_get_content_action_with_file(self, data_tester):
        response = data_tester.get('/path/file.json?action=content')
        assert response.data == b'{"test": "json"}'

    def test_get_content_action_with_invalid_file(self, data_tester):
        response = data_tester.get('/path/file2.json?action=content')
        error = error_from_response(response)
        assert error == INVALID_PATH

    def test_get_content_action_with_dir(self, data_tester):
        response = data_tester.get('/path/subdirectory?action=content')
        assert response.headers['Content-Type'] == 'application/gzip'

    def test_get_content_action_with_invalid_dir(self, data_tester):
        response = data_tester.get(
            '/path/dir_that_does_not_exist?action=content')
        error = error_from_response(response)
        assert error == INVALID_PATH

    def test_get_properties_action_with_file(self, data_tester, file_object):
        response = data_tester.get('/path/file.json?action=properties')
        path = PathSchema().load(load_json_data(response)).data
        assert path == file_object

    def test_get_properties_action_with_dir(self, data_tester, dir_object):
        response = data_tester.get('/path/subdirectory?action=properties')
        path = PathSchema().load(load_json_data(response)).data
        assert path == dir_object

    def test_get_exists_action(self, data_tester):
        response = data_tester.get('/path/empty_dir?action=exists')
        booleanResponse = BooleanResponseSchema().load(
            load_json_data(response)).data
        assert booleanResponse.exists is True

    def test_get_exists_action_with_invalid_file(self, data_tester):
        response = data_tester.get('/path/!invalid_F1l3?action=exists')
        booleanResponse = BooleanResponseSchema().load(
            load_json_data(response)).data
        assert booleanResponse.exists is False

    def test_get_list_action_with_dir(self, data_tester):
        requested_path = 'subdirectory'
        response = data_tester.get(
            '/path/{}?action=list'.format(requested_path))
        paths = PathSchema(many=True).load(load_json_data(response)).data
        expected_paths_list = os.listdir(
            os.path.join(app.config['DATA_DIRECTORY'], 'subdirectory'))
        assert len(expected_paths_list) == len(paths)

    def test_get_list_action_with_file(self, data_tester):
        response = data_tester.get('/path/file.json?action=list')
        error = error_from_response(response)
        assert error == LIST_ACTION_ON_FILE

    def test_get_md5_action_with_file(self, data_tester):
        response = data_tester.get('/path/file.json?action=md5')
        md5 = PathMD5Schema().load(load_json_data(response)).data
        assert md5 == generate_md5(
            os.path.join(app.config['DATA_DIRECTORY'], "file.json"))

    def test_get_md5_action_with_dir(self, data_tester):
        response = data_tester.get('/path/subdirectory?action=md5')
        error = error_from_response(response)
        assert error == MD5_ON_DIR

    # tests for PUT
    def test_put_outside_authorized_directory(self, data_tester):
        response = data_tester.put('/path/../../test_file')
        error = error_from_response(response)
        assert error == UNAUTHORIZED

    def test_put_with_invalid_upload_type(self, data_tester):
        response = data_tester.put(
            '/path/new_file.txt', data='{"type": "Invented"}')
        error = error_from_response(response)
        assert error == INVALID_UPLOAD_TYPE

    # TODO: Uncomment when @marshal_request has option for allow_none
    #  def test_put_invalid_request(self, data_tester):
    #      response = data_tester.put(
    #          '/path/new_file2.txt',
    #          data='{"tyyype": "File", "base64Content": "IL54"}')
    #      error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
    #      assert error == INVALID_UPLOAD_TYPE

    def test_put_where_parent_dir_not_exist(self, data_tester):
        response = data_tester.put('/path/made_up_dir/file.txt')
        error = error_from_response(response)
        assert error == INVALID_PATH

    def test_put_without_content_creates_directory(self, data_tester):
        dir_to_create = 'new_directory'
        response = data_tester.put('/path/new_directory')
        new_dir_path = os.path.join(app.config['DATA_DIRECTORY'],
                                    dir_to_create)
        assert os.path.isdir(new_dir_path)

    def test_put_dir_already_exists(self, data_tester):
        dir_to_create = "subdirectory"
        response = data_tester.put('/path/{}'.format(dir_to_create))
        error = error_from_response(response)
        assert error == INVALID_PATH

    def test_put_base64_file(self, data_tester, put_file):
        file_name = 'put_file.txt'
        response = data_tester.put(
            '/path/{}'.format(file_name),
            data=json.dumps(UploadDataSchema().dump(put_file).data))
        assert os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], file_name))

    def test_put_base64_dir(self, data_tester, put_dir):
        path = '/path/empty_dir'
        abs_path = os.path.join(app.config['DATA_DIRECTORY'], 'empty_dir')
        response = data_tester.put(
            path, data=json.dumps(UploadDataSchema().dump(put_dir).data))
        assert response.status_code == 201 and os.listdir(abs_path)

    def test_put_base64_invalid_dir(self, data_tester):
        path = '/path/empty_dir'
        abs_path = os.path.join(app.config['DATA_DIRECTORY'], 'empty_dir')
        put_dir = UploadData(
            base64_content='bad_content', upload_type='Archive', md5='')
        response = data_tester.put(
            path, data=json.dumps(UploadDataSchema().dump(put_dir).data))
        assert response.status_code == 400

    # tests for DELETE
    def test_delete_single_file(self, data_tester):
        file_to_delete = "file.json"
        response = data_tester.delete('/path/{}'.format(file_to_delete))
        assert (not os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], file_to_delete))
                and response.status_code == 204)

    def test_delete_non_empty_directory(self, data_tester):
        directory_to_delete = "subdirectory"
        response = data_tester.delete('/path/{}'.format(directory_to_delete))
        assert (not os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], directory_to_delete))
                and response.status_code == 204)

    def test_delete_empty_directory(self, data_tester):
        directory_to_delete = "empty_dir"
        response = data_tester.delete('/path/{}'.format(directory_to_delete))
        assert (not os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], directory_to_delete))
                and response.status_code == 204)

    def test_delete_invalid_file(self, data_tester):
        file_to_delete = "does_not_exist"
        response = data_tester.delete('/path/{}'.format(file_to_delete))
        assert response.status_code == 400

    def test_delete_root_directory(self, data_tester):
        directory_to_delete = "./"
        response = data_tester.delete('/path/{}'.format(directory_to_delete))
        assert (os.path.exists(
            app.config['DATA_DIRECTORY'])) and response.status_code == 403

    def test_delete_parent_directory(self, data_tester):
        directory_to_delete = "../.."
        response = data_tester.delete('/path/{}'.format(directory_to_delete))
        assert os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'],
                         directory_to_delete)) and response.status_code == 403
