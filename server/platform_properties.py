from server.common.error_codes_and_messages import errors_as_list
from server.resources.models.platform_properties import PlatformProperties
from server.resources.models.error_code_and_message import ErrorCodeAndMessageSchema

PLATFORM_PROPERTIES = {
    "platformName":
    "CARMIN Server 0.1",
    "APIErrorCodesAndMessages":
    ErrorCodeAndMessageSchema(many=True).dump(errors_as_list()).data,
    "supportedTransferProtocols": ["http", "https"],
    "supportedModules": ["Processing", "Data", "AdvancedData"],
    "defaultLimitListExecutions":
    10,
    "email":
    "carmin@googlegroups.com",
    "platformDescription":
    "A lightweight implementation of the CARMIN 0.3 API Specification",
    "minAuthorizedExecutionTimeout":
    2,
    "maxAuthorizedExecutionTimeout":
    0,
    "defaultExecutionTimeout":
    16384,
    "unsupportedMethods": ["Management", "Commercial"],
    "supportedAPIVersion":
    "0.3",
    "supportedPipelineProperties": ["Prop1", "Prop2", "Prop3"]
}
