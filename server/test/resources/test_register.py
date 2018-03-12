import pytest
import os
import copy
from server import app
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.common.error_codes_and_messages import (
    INVALID_API_KEY, UNAUTHORIZED, MISSING_API_KEY, USERNAME_ALREADY_EXISTS,
    UNEXPECTED_ERROR)
from server.test.utils import get_test_config, json_request_data, load_json_data
from server.test.fakedata.users import admin, standard_user, standard_user_2
from server.database.models.user import User


@pytest.yield_fixture
def test_config(tmpdir_factory):
    test_config = get_test_config()
    test_config.db.session.add(admin(True))
    test_config.db.session.add(standard_user(True))
    test_config.db.session.commit()

    root_directory = tmpdir_factory.mktemp('data')
    app.config['DATA_DIRECTORY'] = str(root_directory)

    yield test_config

    test_config.db.drop_all()


@pytest.yield_fixture
def test_user():
    return {
        "username": standard_user_2().username,
        "password": standard_user_2().password
    }


class TestRegisterResource():
    def test_register_missing_api_key(self, test_config, test_user):
        response = test_config.test_client.post(
            "/users/register",
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == MISSING_API_KEY

    def test_register_invalid_api_key(self, test_config, test_user):
        response = test_config.test_client.post(
            "/users/register",
            headers={"apiKey": "NOT_{}".format(admin().api_key)},
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == INVALID_API_KEY

    def test_register_user_api_key(self, test_config, test_user):
        response = test_config.test_client.post(
            "/users/register",
            headers={"apiKey": standard_user().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == UNAUTHORIZED

    def test_register_successful(self, test_config, test_user):
        response = test_config.test_client.post(
            "/users/register",
            headers={"apiKey": admin().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        assert response.status_code == 204
        assert os.path.exists(
            os.path.join(app.config['DATA_DIRECTORY'], test_user["username"]))

    def test_register_successful_and_login(self, test_config, test_user):
        response = test_config.test_client.post(
            "/users/register",
            headers={"apiKey": admin().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        assert response.status_code == 204

        response = test_config.test_client.post(
            "/authenticate",
            data=json_request_data(test_user),
            follow_redirects=True)

        assert response.status_code == 200

    def test_register_already_existing_username(self, test_config, test_user):
        response = test_config.test_client.post(
            "/users/register",
            headers={"apiKey": admin().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        assert response.status_code == 204

        response2 = test_config.test_client.post(
            "/users/register",
            headers={"apiKey": admin().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(
            load_json_data(response2)).data

        expected_error_code_and_message = copy.deepcopy(
            USERNAME_ALREADY_EXISTS)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            test_user["username"])
        assert error == expected_error_code_and_message

    def test_register_already_existing_user_folder(self, test_config,
                                                   test_user):
        os.mkdir(
            os.path.join(app.config['DATA_DIRECTORY'], test_user["username"]))

        response = test_config.test_client.post(
            "/users/register",
            headers={"apiKey": admin().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert response.status_code == 500
        assert error == UNEXPECTED_ERROR

        already_existing_user = test_config.db.session.query(User).filter_by(
            username=test_user["username"]).first()

        assert not already_existing_user
