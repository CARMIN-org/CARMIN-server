from marshmallow import Schema, fields, post_load


class ErrorCodeAndMessage():
    """ErrorCodeAndMessage contains an error code along with a human readable 
       error message

    Attributes:
        error_code (int): The error code
        error_message (str): The human readable error message
    """

    def __init__(self, error_code: int = None, error_message: str = None):
        self.error_code = error_code
        self.error_message = error_message


class ErrorCodeAndMessageSchema(Schema):
    error_code = fields.Int(
        required=True, dump_to='errorCode', load_from='errorCode')
    error_message = fields.Str(
        required=True, dump_to='errorMessage', load_from='errorMessage')

    @post_load
    def to_model(self, data):
        return ErrorCodeAndMessage(**data)
