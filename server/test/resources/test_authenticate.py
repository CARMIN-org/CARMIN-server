import pytest
import os
import json
from server.database.models.user import User
from server.test.conftest import test_client, session
from server.test.utils import load_json_data
from server.resources.models.authentication import AuthenticationSchema
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.common.error_codes_and_messages import INVALID_USERNAME_OR_PASSWORD, INVALID_MODEL_PROVIDED
from server.test.fakedata.users import standard_user


@pytest.fixture(autouse=True)
def test_config(session):
    session.add(standard_user(True))
    session.commit()


@pytest.yield_fixture
def test_user():
    return {
        "username": standard_user().username,
        "password": standard_user().password
    }


class TestAuthenticate():
    def test_valid_login(self, test_client, test_user):
        response = test_client.post(
            "/authenticate", data=json.dumps(test_user), follow_redirects=True)

        assert response.status_code == 200

        schema = AuthenticationSchema()
        auth_cred, errors = schema.load(load_json_data(response))

        assert not errors
        assert auth_cred.http_header == "apiKey"

    def test_same_api_key(self, test_client, test_user):
        response = test_client.post(
            "/authenticate", data=json.dumps(test_user), follow_redirects=True)

        assert response.status_code == 200

        schema = AuthenticationSchema()
        auth_cred, errors = schema.load(load_json_data(response))
        assert not errors

        response = test_client.post(
            "/authenticate", data=json.dumps(test_user), follow_redirects=True)

        assert response.status_code == 200

        auth_cred2, errors2 = schema.load(load_json_data(response))
        assert not errors2
        assert auth_cred.http_header_value == auth_cred2.http_header_value

    def test_invalid_username(self, test_client, test_user):
        test_user["username"] = "NOT_{}".format(test_user["username"])

        response = test_client.post(
            "/authenticate", data=json.dumps(test_user), follow_redirects=True)

        assert response.status_code == 400

        schema = ErrorCodeAndMessageSchema()
        ecam, errors = schema.load(load_json_data(response))

        assert not errors
        assert ecam == INVALID_USERNAME_OR_PASSWORD

    def test_invalid_password(self, test_client, test_user):
        test_user["password"] = "NOT_{}".format(test_user["password"])

        response = test_client.post(
            "/authenticate", data=json.dumps(test_user), follow_redirects=True)

        assert response.status_code == 400

        schema = ErrorCodeAndMessageSchema()
        ecam, errors = schema.load(load_json_data(response))

        assert not errors
        assert ecam == INVALID_USERNAME_OR_PASSWORD

    def test_missing_properties(self, test_client):
        response = test_client.post(
            "/authenticate",
            data=json.dumps({
                "notavalid": "NotAValid",
                "invalid": "Invalid"
            }),
            follow_redirects=True)

        assert response.status_code == 400

        schema = ErrorCodeAndMessageSchema()
        ecam, errors = schema.load(load_json_data(response))

        assert not errors
        assert ecam.error_code == INVALID_MODEL_PROVIDED.error_code
        assert ecam.error_message == INVALID_MODEL_PROVIDED.error_message
        assert len(ecam.error_detail) == 2
        assert "username" in ecam.error_detail
        assert "password" in ecam.error_detail
