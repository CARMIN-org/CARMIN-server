import pytest
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.common.error_codes_and_messages import INVALID_API_KEY, UNAUTHORIZED, MISSING_API_KEY
from server.test.utils import get_test_config, json_request_data, load_json_data
from server.test.fakedata.users import admin, standard_user


@pytest.yield_fixture
def test_config_client(tmpdir_factory):
    test_config = get_test_config()
    test_config.db.session.add(admin())
    test_config.db.session.add(standard_user())
    test_config.db.session.commit()

    yield test_config.test_client

    test_config.db.drop_all()


@pytest.yield_fixture
def test_user():
    return {"username": "newTestUser", "password": "ImpressiveP±ssw0rd"}


class TestRegisterResource():
    def test_register_missing_api_key(self, test_config_client, test_user):
        response = test_config_client.post(
            "/users/register",
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == MISSING_API_KEY

    def test_register_invalid_api_key(self, test_config_client, test_user):
        response = test_config_client.post(
            "/users/register",
            headers={"apiKey": "NOT_{}".format(admin().api_key)},
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == INVALID_API_KEY

    def test_register_user_api_key(self, test_config_client, test_user):
        response = test_config_client.post(
            "/users/register",
            headers={"apiKey": standard_user().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        error = ErrorCodeAndMessageSchema().load(load_json_data(response)).data
        assert error == UNAUTHORIZED

    def test_register_successful(self, test_config_client, test_user):
        response = test_config_client.post(
            "/users/register",
            headers={"apiKey": admin().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        assert response.status_code == 204

    def test_register_successful_and_login(self, test_config_client,
                                           test_user):
        response = test_config_client.post(
            "/users/register",
            headers={"apiKey": admin().api_key},
            data=json_request_data(test_user),
            follow_redirects=True)
        assert response.status_code == 204

        response = test_config_client.post(
            "/authenticate",
            data=json_request_data(test_user),
            follow_redirects=True)

        assert response.status_code == 200