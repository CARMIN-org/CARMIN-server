from marshmallow import Schema, fields, post_load


class BooleanResponse():
    def __init__(self, exists: bool):
        self.exists = exists

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class BooleanResponseSchema(Schema):
    class Meta:
        ordered = True

    exists = fields.Boolean(required=True)

    @post_load
    def to_model(self, data):
        return BooleanResponse(**data)
