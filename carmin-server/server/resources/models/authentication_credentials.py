from marshmallow import Schema, fields, post_load


class AuthenticationCredentials():
    """AuthenticationCredentials

    Args:
        username (str):
        password (str):

    Attributes:
        username (str):
        password (str):
    """

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password


class AuthenticationCredentialsSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @post_load
    def to_model(self, data):
        return AuthenticationCredentials(**data)
