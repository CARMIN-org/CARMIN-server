from marshmallow import Schema, fields, post_load, post_dump

PARAMETER_TYPES = ["File", "String", "Boolean", "Int64", "Double", "List"]


class PipelineParameterSchema(Schema):
    SKIP_VALUES = list([None])

    class Meta:
        ordered = True

    name = fields.Str(required=True)
    parameter_type = fields.Str(
        required=True,
        dump_to='type',
        load_from='type',
        validate=lambda pt: pt in PARAMETER_TYPES)
    is_optional = fields.Bool(
        required=True, dump_to='isOptional', load_from='isOptional')
    is_returned_value = fields.Bool(
        required=True, dump_to='isReturnedValue', load_from='isReturnedValue')
    default_value = fields.Str(
        dump_to='defaultValue', load_from='defaultValue')
    description = fields.Str()

    @post_load
    def to_model(self, data):
        return PipelineParameter(**data)

    @post_dump
    def remove_skip_values(self, data):
        """remove_skip_values removes all values specified in the
        SKIP_VALUES set from appearing in the 'dumped' JSON.
        """
        return {
            key: value
            for key, value in data.items() if value not in self.SKIP_VALUES
        }


class PipelineParameter():
    schema = PipelineParameterSchema()

    def __init__(self,
                 name: str = None,
                 parameter_type: str = None,
                 is_optional: bool = None,
                 is_returned_value: bool = None,
                 default_value: str = None,
                 description: str = None):

        self.name = name
        self.parameter_type = parameter_type
        self.is_optional = is_optional
        self.is_returned_value = is_returned_value
        self.default_value = default_value
        self.description = description

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
