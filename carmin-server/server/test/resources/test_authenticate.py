import pytest
import os
from unittest import TestCase

from server.database.models.user import User
from server.test.utils import get_test_config, json_request_data, load_json_data
from server.resources.models.authentication import AuthenticationSchema
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema
from server.common.error_codes_and_messages import INVALID_USERNAME_OR_PASSWORD, INVALID_MODEL_PROVIDED


class TestDecorator(TestCase):
    def setUp(self):
        self.app, self.db = get_test_config()

    def tearDown(self):
        self.db.drop_all()

    def test_valid_login(self):
        user = User(username="NiceTestUser", password="ImpressiveP±ssw0rd")
        self.db.session.add(user)
        self.db.session.commit()

        response = self.app.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        schema = AuthenticationSchema()
        auth_cred, errors = schema.load(load_json_data(response))

        self.assertFalse(errors)
        self.assertEqual(auth_cred.http_header, "apiKey")

    def test_same_api_key(self):
        user = User(username="NiceTestUser", password="ImpressiveP±ssw0rd")
        self.db.session.add(user)
        self.db.session.commit()

        response = self.app.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        schema = AuthenticationSchema()
        auth_cred, errors = schema.load(load_json_data(response))
        self.assertFalse(errors)

        response = self.app.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        auth_cred2, errors2 = schema.load(load_json_data(response))
        self.assertFalse(errors2)
        self.assertEqual(auth_cred.http_header_value,
                         auth_cred2.http_header_value)

    def test_invalid_username(self):
        user = User(username="NiceTestUser", password="ImpressiveP±ssw0rd")
        self.db.session.add(user)
        self.db.session.commit()

        response = self.app.post(
            "/authenticate",
            data=json_request_data({
                "username": "UnexistantUsername",
                "password": "ImpressiveP±ssw0rd"
            }),
            follow_redirects=True)

        self.assertEqual(response.status_code, 400)

        schema = ErrorCodeAndMessageSchema()
        ecas, errors = schema.load(load_json_data(response))

        self.assertFalse(errors)
        self.assertEqual(ecas.error_code,
                         INVALID_USERNAME_OR_PASSWORD.error_code)
        self.assertEqual(ecas.error_message,
                         INVALID_USERNAME_OR_PASSWORD.error_message)

    def test_invalid_password(self):
        user = User(username="NiceTestUser", password="ImpressiveP±ssw0rd")
        self.db.session.add(user)
        self.db.session.commit()

        response = self.app.post(
            "/authenticate",
            data=json_request_data({
                "username": "NiceTestUser",
                "password": "NotTheRightPassword"
            }),
            follow_redirects=True)

        self.assertEqual(response.status_code, 400)

        schema = ErrorCodeAndMessageSchema()
        ecas, errors = schema.load(load_json_data(response))

        self.assertFalse(errors)
        self.assertEqual(ecas.error_code,
                         INVALID_USERNAME_OR_PASSWORD.error_code)
        self.assertEqual(ecas.error_message,
                         INVALID_USERNAME_OR_PASSWORD.error_message)

    def test_missing_properties(self):
        response = self.app.post(
            "/authenticate",
            data=json_request_data({
                "notavalid": "NotAValid",
                "invalid": "Invalid"
            }),
            follow_redirects=True)

        self.assertEqual(response.status_code, 400)

        schema = ErrorCodeAndMessageSchema()
        ecas, errors = schema.load(load_json_data(response))

        self.assertFalse(errors)
        self.assertEqual(ecas.error_code, INVALID_MODEL_PROVIDED.error_code)
        self.assertEqual(ecas.error_message,
                         INVALID_MODEL_PROVIDED.error_message)
        self.assertEqual(len(ecas.error_detail), 2)
        self.assertIn("username", ecas.error_detail)
        self.assertIn("password", ecas.error_detail)
