from marshmallow import Schema, fields, post_load, validate


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
    class Meta:
        ordered = True

    username = fields.Str(
        required=True,
        validate=validate.Regexp("^[a-zA-Z0-9_\-]*$", 0,
                                 "'{input}' contains illegal characters."))
    password = fields.Str(required=True)

    @post_load
    def to_model(self, data):
        return AuthenticationCredentials(**data)
