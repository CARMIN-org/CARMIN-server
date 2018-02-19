from marshmallow import Schema, fields, post_load


class ErrorCodeAndMessage():
    """ErrorCodeAndMessage contains an error code along with a human readable 
       error message

    Attributes:
        error_code (int): The error code
        error_message (str): The human readable error message
        error_detail (dict, optional): Additional error details
    """

    def __init__(self,
                 error_code: int = None,
                 error_message: str = None,
                 error_detail: dict = dict()):
        self.error_code = error_code
        self.error_message = error_message
        self.error_detail = error_detail

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ErrorCodeAndMessageSchema(Schema):
    class Meta:
        ordered = True

    error_code = fields.Int(
        required=True, dump_to='errorCode', load_from='errorCode')
    error_message = fields.Str(
        required=True, dump_to='errorMessage', load_from='errorMessage')
    error_detail = fields.Dict(dump_to='errorDetail', load_from='errorDetail')

    @post_load
    def to_model(self, data):
        return ErrorCodeAndMessage(**data)
