import pytest
import copy
import json
import os
from server import app
from server.common.error_codes_and_messages import (
    USER_DOES_NOT_EXIST, UNAUTHORIZED, INVALID_MODEL_PROVIDED)
from server.test.utils import error_from_response
from server.test.conftest import test_client, session
from server.test.fakedata.users import admin, standard_user, standard_user_2


@pytest.fixture(autouse=True)
def test_config(tmpdir_factory, session):
    session.add(admin(True))
    session.add(standard_user(True))
    session.add(standard_user_2(True))
    session.commit()

    root_directory = tmpdir_factory.mktemp('data')
    app.config['DATA_DIRECTORY'] = str(root_directory)


class TestEditResource():
    def test_edit_password_admin(self, test_client):
        response = test_client.post(
            "/users/edit",
            headers={"apiKey": admin().api_key},
            data=json.dumps({
                "username": standard_user().username,
                "password": standard_user().password + "2"
            }))
        assert response.status_code == 200

        response = test_client.post(
            "/authenticate",
            data=json.dumps({
                "username": standard_user().username,
                "password": standard_user().password + "2"
            }))
        assert response.status_code == 200

    def test_edit_password_user_not_exist(self, test_client):
        response = test_client.post(
            "/users/edit",
            headers={"apiKey": admin().api_key},
            data=json.dumps({
                "username": "does_not_exist",
                "password": standard_user().password + "2"
            }))
        error = error_from_response(response)
        expected_error_code_and_message = copy.deepcopy(USER_DOES_NOT_EXIST)
        expected_error_code_and_message.error_message = expected_error_code_and_message.error_message.format(
            "does_not_exist")
        assert error == expected_error_code_and_message

    def test_edit_own_password_admin(self, test_client):
        response = test_client.post(
            "/users/edit",
            headers={"apiKey": admin().api_key},
            data=json.dumps({
                "password": standard_user().password + "2"
            }))
        assert response.status_code == 200

        response = test_client.post(
            "/authenticate",
            data=json.dumps({
                "username": admin().username,
                "password": standard_user().password + "2"
            }))
        assert response.status_code == 200

    def test_edit_password_user(self, test_client):
        response = test_client.post(
            "/users/edit",
            headers={"apiKey": standard_user().api_key},
            data=json.dumps({
                "password": standard_user().password + "2"
            }))
        assert response.status_code == 200

        response = test_client.post(
            "/authenticate",
            data=json.dumps({
                "username": standard_user().username,
                "password": standard_user().password + "2"
            }))
        assert response.status_code == 200

    def test_edit_password_user_other_user(self, test_client):
        response = test_client.post(
            "/users/edit",
            headers={"apiKey": standard_user().api_key},
            data=json.dumps({
                "username": standard_user_2().username,
                "password": standard_user().password + "2"
            }))
        error = error_from_response(response)
        assert error == UNAUTHORIZED

    def test_edit_password_no_password(self, test_client):
        response = test_client.post(
            "/users/edit",
            headers={"apiKey": standard_user().api_key},
            data=json.dumps({
                "password": ""
            }))
        error = error_from_response(response)
        INVALID_MODEL_PROVIDED.error_detail = "'password' is required"
        assert error == INVALID_MODEL_PROVIDED
