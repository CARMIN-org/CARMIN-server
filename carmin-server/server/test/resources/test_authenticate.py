import pytest
import os
from unittest import TestCase
from server.database.models.user import User
from server.test.utils import get_test_config, json_request_data, load_json_data
from server.resources.models.authentication import AuthenticationSchema
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.common.error_codes_and_messages import INVALID_USERNAME_OR_PASSWORD, INVALID_MODEL_PROVIDED


@pytest.yield_fixture(scope="module")
def test_config(tmpdir_factory):
    test_config = get_test_config()

    user = User(username="NiceTestUser", password="ImpressiveP±ssw0rd")
    test_config.db.session.add(user)
    test_config.db.session.commit()

    yield test_config

    test_config.db.drop_all()


class TestAuthenticate():
    def test_valid_login(self, test_config):
        response = test_config.test_client.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        assert response.status_code == 200

        schema = AuthenticationSchema()
        auth_cred, errors = schema.load(load_json_data(response))

        assert not errors
        assert auth_cred.http_header == "apiKey"

    def test_same_api_key(self, test_config):
        response = test_config.test_client.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        assert response.status_code == 200

        schema = AuthenticationSchema()
        auth_cred, errors = schema.load(load_json_data(response))
        assert not errors

        response = test_config.test_client.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        assert response.status_code == 200

        auth_cred2, errors2 = schema.load(load_json_data(response))
        assert not errors2
        assert auth_cred.http_header_value == auth_cred2.http_header_value

    def test_invalid_username(self, test_config):
        response = test_config.test_client.post(
            "/authenticate",
            data=json_request_data({
                "username": "UnexistantUsername",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        assert response.status_code == 400

        schema = ErrorCodeAndMessageSchema()
        ecam, errors = schema.load(load_json_data(response))

        assert not errors
        assert ecam == INVALID_USERNAME_OR_PASSWORD

    def test_invalid_password(self, test_config):
        response = test_config.test_client.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "NotTheRightPassword"
            }),
            follow_redirects=True)

        assert response.status_code == 400

        schema = ErrorCodeAndMessageSchema()
        ecam, errors = schema.load(load_json_data(response))

        assert not errors
        assert ecam == INVALID_USERNAME_OR_PASSWORD

    def test_missing_properties(self, test_config):
        response = test_config.test_client.post(
            "/authenticate",
            data=json_request_data({
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
