import pytest
import os
import json
import zipfile
from server import app
from server.config import TestConfig
from server.test.utils import load_json_data, error_from_response
from server.test.conftest import test_client, session
from server.common.error_codes_and_messages import (
    MD5_ON_DIR, INVALID_PATH, UNAUTHORIZED, ACTION_REQUIRED, INVALID_ACTION,
    LIST_ACTION_ON_FILE, INVALID_MODEL_PROVIDED, PATH_EXISTS,
    INVALID_UPLOAD_TYPE, PATH_DOES_NOT_EXIST, PATH_IS_DIRECTORY)
from server.resources.models.path import Path, PathSchema
from server.resources.models.path_md5 import PathMD5Schema
from server.resources.models.upload_data import UploadData, UploadDataSchema
from server.resources.models.boolean_response import BooleanResponseSchema
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.resources.path import generate_md5
from server.test.fakedata.users import standard_user


@pytest.fixture(autouse=True)
def test_config(tmpdir_factory, session):
    session.add(standard_user(True))
    session.commit()

    root_directory = tmpdir_factory.mktemp('data')
    subdir = root_directory.mkdir(standard_user().username)

    subdir.mkdir('empty_dir')
    subdir.mkdir('subdirectory')
    subdir.join('subdir_text.txt').write(
        "this is a text file inside data/subdir")
    subdir.join('test.txt').write("content")
    subdir.join('file.json').write('{"test": "json"}')
    subdir.join('directory.yml').write("-yaml file")
    app.config['DATA_DIRECTORY'] = str(root_directory)


@pytest.fixture
def file_object():
    file_path = os.path.join(app.config['DATA_DIRECTORY'],
                             '{}/file.json'.format(standard_user().username))
    return Path(
        platform_path="http://localhost/path/{}/file.json".format(
            standard_user().username),
        last_modification_date=int(os.path.getmtime(file_path)),
        is_directory=False,
        size=Path.get_path_size(file_path, is_dir=False),
        mime_type='application/json')


@pytest.fixture
def dir_object():
    dir_path = os.path.join(app.config['DATA_DIRECTORY'],
                            '{}/subdirectory'.format(standard_user().username))
    return Path(
        platform_path="http://localhost/path/{}/subdirectory".format(
            standard_user().username),
        last_modification_date=int(os.path.getmtime(dir_path)),
        is_directory=True,
        size=Path.get_path_size(dir_path, is_dir=True),
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

    def test_query_outside_authorized_directory(self, test_client):
        response = test_client.get(
            '/path/../../test?action=properties',
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == INVALID_PATH

    def test_get_no_action(self, test_client):
        response = test_client.get(
            '/path/{}/file.json'.format(standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == ACTION_REQUIRED

    def test_get_invalid_action(self, test_client):
        response = test_client.get(
            '/path/{}/file.json?action=invalid'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == INVALID_ACTION

    def test_get_content_action_with_file(self, test_client):
        response = test_client.get(
            '/path/{}/file.json?action=content'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        assert response.data == b'{"test": "json"}'

    def test_get_content_action_with_invalid_file(self, test_client):
        response = test_client.get(
            '/path/{}/file2.json?action=content'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == PATH_DOES_NOT_EXIST

    def test_get_content_action_with_dir(self, test_client):
        response = test_client.get(
            '/path/{}/subdirectory?action=content'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        assert response.headers['Content-Type'] == 'application/gzip'

    def test_get_content_action_with_invalid_dir(self, test_client):
        response = test_client.get(
            '/path/{}/dir_that_does_not_exist?action=content'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == PATH_DOES_NOT_EXIST

    def test_get_properties_action_with_file(self, test_client, file_object):
        response = test_client.get(
            '/path/{}/file.json?action=properties'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        path = PathSchema().load(load_json_data(response)).data
        assert path == file_object

    def test_get_properties_action_with_dir(self, test_client, dir_object):
        response = test_client.get(
            '/path/{}/subdirectory?action=properties'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        path = PathSchema().load(load_json_data(response)).data
        assert path == dir_object

    def test_get_exists_action(self, test_client):
        response = test_client.get(
            '/path/{}/empty_dir?action=exists'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        booleanResponse = BooleanResponseSchema().load(
            load_json_data(response)).data
        assert booleanResponse.exists is True

    def test_get_exists_action_with_invalid_file(self, test_client):
        response = test_client.get(
            '/path/{}/!invalid_F1l3?action=exists'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        booleanResponse = BooleanResponseSchema().load(
            load_json_data(response)).data
        assert booleanResponse.exists is False

    def test_get_list_action_with_dir(self, test_client):
        response = test_client.get(
            '/path/{}/subdirectory?action=list'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        paths = PathSchema(many=True).load(load_json_data(response)).data
        expected_paths_list = os.listdir(
            os.path.join(app.config['DATA_DIRECTORY'],
                         '{}/subdirectory'.format(standard_user().username)))
        assert len(expected_paths_list) == len(paths)

    def test_get_list_action_with_file(self, test_client):
        response = test_client.get(
            '/path/{}/file.json?action=list'.format(standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == LIST_ACTION_ON_FILE

    def test_get_md5_action_with_file(self, test_client):
        response = test_client.get(
            '/path/{}/file.json?action=md5'.format(standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        md5 = PathMD5Schema().load(load_json_data(response)).data
        assert md5 == generate_md5(
            os.path.join(app.config['DATA_DIRECTORY'], "{}/file.json".format(
                standard_user().username)))

    def test_get_md5_action_with_dir(self, test_client):
        response = test_client.get(
            '/path/{}/subdirectory?action=md5'.format(
                standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == MD5_ON_DIR

    # tests for PUT
    def test_put_outside_authorized_directory(self, test_client):
        response = test_client.put(
            '/path/../../test_file',
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == INVALID_PATH

    def test_put_with_invalid_upload_type(self, test_client):
        response = test_client.put(
            '/path/{}/new_file.txt'.format(standard_user().username),
            headers={"apiKey": standard_user().api_key},
            data='{"type": "Invented", "base64Content": "ewlfkjweflk=="}')
        error = error_from_response(response)
        assert error.error_code == INVALID_MODEL_PROVIDED.error_code
        assert error.error_message == INVALID_MODEL_PROVIDED.error_message
        assert len(error.error_detail) == 1
        assert "type" in error.error_detail


    def test_put_where_parent_dir_not_exist(self, test_client):
        response = test_client.put(
            '/path/{}/made_up_dir/file.txt'.format(standard_user().username),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == INVALID_PATH

    def test_put_without_content_creates_directory(self, test_client):
        dir_to_create = '{}/new_directory'.format(standard_user().username)
        response = test_client.put(
            '/path/{}'.format(dir_to_create),
            headers={
                "apiKey": standard_user().api_key
            })
        new_dir_path = os.path.join(app.config['DATA_DIRECTORY'],
                                    dir_to_create)
        assert os.path.isdir(new_dir_path)

    def test_put_dir_already_exists(self, test_client):
        dir_to_create = "{}/subdirectory".format(standard_user().username)
        response = test_client.put(
            '/path/{}'.format(dir_to_create),
            headers={
                "apiKey": standard_user().api_key
            })
        error = error_from_response(response)
        assert error == PATH_EXISTS

    def test_put_base64_file(self, test_client, put_file):
        file_name = '{}/put_file.txt'.format(standard_user().username)
        response = test_client.put(
            '/path/{}'.format(file_name),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(UploadDataSchema().dump(put_file).data))
        assert os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], file_name))

    def test_put_base64_dir(self, test_client, put_dir):
        path = '{}/empty_dir'.format(standard_user().username)
        abs_path = os.path.join(app.config['DATA_DIRECTORY'], path)
        response = test_client.put(
            '/path/{}'.format(path),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(UploadDataSchema().dump(put_dir).data))
        assert response.status_code == 201 and os.listdir(abs_path)

    def test_put_base64_invalid_dir(self, test_client):
        path = '{}/empty_dir2'.format(standard_user().username)
        abs_path = os.path.join(app.config['DATA_DIRECTORY'], path)
        put_dir = UploadData(
            base64_content='bad_content', upload_type='Archive', md5='')
        response = test_client.put(
            '/path/{}'.format(path),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(UploadDataSchema().dump(put_dir).data))
        assert response.status_code == 400

    def test_put_file_on_dir(self, test_client):
        path = '{}/empty_dir'.format(standard_user().username)
        put_dir = UploadData(
            base64_content='bad_content', upload_type='File', md5='')
        response = test_client.put(
            '/path/{}'.format(path),
            headers={"apiKey": standard_user().api_key},
            data=json.dumps(UploadDataSchema().dump(put_dir).data))
        error = error_from_response(response)
        assert error.error_message == "Invalid path: '{}' is a directory.".format(
            path)

    # tests for DELETE
    def test_delete_single_file(self, test_client):
        file_to_delete = "{}/file.json".format(standard_user().username)
        response = test_client.delete(
            '/path/{}'.format(file_to_delete),
            headers={
                "apiKey": standard_user().api_key
            })
        assert (not os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], file_to_delete))
                and response.status_code == 204)

    def test_delete_non_empty_directory(self, test_client):
        directory_to_delete = "{}/subdirectory".format(
            standard_user().username)
        response = test_client.delete(
            '/path/{}'.format(directory_to_delete),
            headers={
                "apiKey": standard_user().api_key
            })
        assert (not os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], directory_to_delete))
                and response.status_code == 204)

    def test_delete_empty_directory(self, test_client):
        directory_to_delete = "{}/empty_dir".format(standard_user().username)
        response = test_client.delete(
            '/path/{}'.format(directory_to_delete),
            headers={
                "apiKey": standard_user().api_key
            })
        assert (not os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], directory_to_delete))
                and response.status_code == 204)

    def test_delete_invalid_file(self, test_client):
        file_to_delete = "{}/does_not_exist".format(standard_user().username)
        response = test_client.delete(
            '/path/{}'.format(file_to_delete),
            headers={
                "apiKey": standard_user().api_key
            })
        assert response.status_code == 400

    def test_delete_root_directory(self, test_client):
        directory_to_delete = "./"
        response = test_client.delete(
            '/path/{}'.format(directory_to_delete),
            headers={
                "apiKey": standard_user().api_key
            })
        assert (os.path.exists(
            app.config['DATA_DIRECTORY'])) and response.status_code == 403

    def test_delete_parent_directory(self, test_client):
        directory_to_delete = "../.."
        response = test_client.delete(
            '/path/{}'.format(directory_to_delete),
            headers={
                "apiKey": standard_user().api_key
            })
        assert os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'],
                         directory_to_delete)) and response.status_code == 403
