from typing import List

from .error_code_and_message import ErrorCodeAndMessageSchema, ErrorCodeAndMessage
from .pipeline_parameter import PipelineParameterSchema, PipelineParameter

from marshmallow import Schema, fields, post_load, post_dump


class Pipeline():
    def __init__(self,
                 identifier: str = None,
                 name: str = None,
                 version: str = None,
                 description: str = None,
                 can_execute: bool = None,
                 parameters: List[PipelineParameter] = None,
                 properties: object = None,
                 error_codes_and_messages: List[ErrorCodeAndMessage] = None):

        self.identifier = identifier
        self.name = name
        self.version = version
        self.description = description
        self.can_execute = can_execute
        self.parameters = parameters
        self.properties = properties
        self.error_codes_and_messages = error_codes_and_messages

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PipelineSchema(Schema):
    SKIP_VALUES = list([None])

    class Meta:
        ordered = True

    identifier = fields.Str(required=True)
    name = fields.Str(required=True)
    version = fields.Str(required=True)
    description = fields.Str()
    can_execute = fields.Bool(dump_to='canExecute', load_from='canExecute')
    parameters = fields.Nested(PipelineParameterSchema, many=True)
    properties = fields.Dict()
    error_codes_and_messages = fields.Nested(
        ErrorCodeAndMessageSchema,
        dump_to='errorCodesAndMessages',
        load_from='errorCodesAndMessages',
        many=True)

    @post_load
    def to_model(self, data):
        return Pipeline(**data)

    @post_dump
    def remove_skip_values(self, data):
        """remove_skip_values removes all values specified in the
        SKIP_VALUES set from appearing in the 'dumped' JSON.
        """
        return {
            key: value
            for key, value in data.items() if value not in self.SKIP_VALUES
        }
