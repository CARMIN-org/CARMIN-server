from marshmallow import Schema, fields, post_load


class BooleanResponseSchema(Schema):
    class Meta:
        ordered = True

    exists = fields.Boolean(required=True)

    @post_load
    def to_model(self, data):
        return BooleanResponse(**data)


class BooleanResponse():
    schema = BooleanResponseSchema()

    def __init__(self, exists: bool):
        self.exists = exists

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
