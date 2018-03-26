from typing import List
from .error_code_and_message import ErrorCodeAndMessage, ErrorCodeAndMessageSchema

from marshmallow import Schema, fields, post_load


class PlatformPropertiesSchema(Schema):
    class Meta:
        ordered = True

    platform_name = fields.Str(
        dump_to='platformName', load_from='platformName')
    api_error_codes_and_messages = fields.Nested(
        ErrorCodeAndMessageSchema,
        many=True,
        dump_to='APIErrorCodesAndMessage',
        load_from='APIErrorCodesAndMessages')
    supported_transfer_protocols = fields.List(
        fields.Str(),
        required=True,
        dump_to='supportedTransferProtocols',
        load_from='supportedTransferProtocols')
    supported_modules = fields.List(
        fields.Str(),
        required=True,
        dump_to='supportedModules',
        load_from='supportedModules')
    default_limit_list_executions = fields.Int(
        dump_to='defaultLimitListExecutions',
        load_from='defaultLimitListExecutions')
    email = fields.Str()
    platform_description = fields.Str(
        dump_to='platformDescription', load_from='platformDescription')
    min_authorized_execution_timeout = fields.Int(
        dump_to='minAuthorizedExecutionTimeout',
        load_from='minAuthorizedExecutionTimeout')
    max_authorized_execution_timeout = fields.Int(
        dump_to='maxAuthorizedExecutionTimeout',
        load_from='maxAuthorizedExecutionTimeout')
    default_execution_timeout = fields.Int(
        dump_to='defaultExecutionTimeout', load_from='defaultExecutionTimeout')
    unsupported_methods = fields.List(
        fields.Str(),
        dump_to='unsupportedMethods',
        load_from='unsupportedMethods')
    default_study = fields.Str(
        dump_to='defaultStudy', load_from='defaultStudy')
    supported_api_version = fields.Str(
        required=True,
        dump_to='supportedAPIVersion',
        load_from='supportedAPIVersion')
    supported_pipeline_properties = fields.List(
        fields.Str(),
        dump_to='supportedPipelineProperties',
        load_from='supportedPipelineProperties')

    @post_load
    def to_model(self, data):
        return PlatformProperties(**data)


class PlatformProperties():
    schema = PlatformPropertiesSchema()

    def __init__(
            self,
            platform_name: str = None,
            api_error_codes_and_messages: List[ErrorCodeAndMessage] = None,
            supported_transfer_protocols: List[str] = None,
            supported_modules: List[str] = None,
            default_limit_list_executions: int = None,
            email: str = None,
            platform_description: str = None,
            min_authorized_execution_timeout: int = 0,
            max_authorized_execution_timeout: int = 0,
            default_execution_timeout: int = 0,
            unsupported_methods: List[str] = None,
            default_study: str = None,
            supported_api_version: str = None,
            supported_pipeline_properties: List[str] = None):

        self.platform_name = platform_name
        self.api_error_codes_and_messages = api_error_codes_and_messages
        self.supported_transfer_protocols = supported_transfer_protocols
        self.supported_modules = supported_modules
        self.default_limit_list_executions = default_limit_list_executions
        self.email = email
        self.platform_description = platform_description
        self.min_authorized_execution_timeout = min_authorized_execution_timeout
        self.max_authorized_execution_timeout = max_authorized_execution_timeout
        self.default_execution_timeout = default_execution_timeout
        self.unsupported_methods = unsupported_methods
        self.default_study = default_study
        self.supported_api_version = supported_api_version
        self.supported_pipeline_properties = supported_pipeline_properties
