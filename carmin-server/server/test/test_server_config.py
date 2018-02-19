from typing import Dict
import pytest
import copy
from server.startup_validation import properties_validation
from server.common.exceptions import MissingRequiredParameterError


@pytest.fixture
def config_data() -> Dict:
    return {
        "platformName":
        "CARMIN Lightweight Server 0.3",
        "APIErrorCodesAndMessages": [{
            "errorCode": 401,
            "errorMessage": "Unauthorized"
        }, {
            "errorCode": 404,
            "errorMessage": "Page not found"
        }],
        "supportedTransferProtocols": ["http", "https"],
        "supportedModules": ["Processing", "Data", "AdvancedData"],
        "defaultLimitListExecutions":
        10,
        "email":
        "carmin@googlegroups.com",
        "platformDescription":
        "A lightweight implementation of the CARMIN 0.3 API Specification",
        "minAuthorizedExecutionTimeout":
        128,
        "maxAuthorizedExecutionTimeout":
        0,
        "defaultExecutionTimeout":
        16384,
        "unsupportedMethods": ["Management", "Commercial"],
        "defaultStudy":
        "COMP490",
        "supportedAPIVersion":
        "0.3",
        "supportedPipelineProperties": ["Prop1", "Prop2", "Prop3"]
    }


def test_missing_required_parameter(config_data):
    del config_data['supportedAPIVersion']
    with pytest.raises(MissingRequiredParameterError):
        properties_validation(config_data)


def test_empty_config_object():
    with pytest.raises(MissingRequiredParameterError):
        properties_validation({})


def test_invalid_protocol(config_data):
    config_data['supportedTransferProtocols'].append("invalidProtocol")
    with pytest.raises(ValueError):
        properties_validation(config_data)


def test_max_authorized_execution_timeout_greater_than_min(config_data):
    config_data['minAuthorizedExecutionTimeout'] = 1024
    config_data['maxAuthorizedExecutionTimeout'] = 64
    with pytest.raises(ValueError):
        properties_validation(config_data)


def test_max_authorized_execution_timeout_zero_value(config_data):
    config_data['minAuthorizedExecutionTimeout'] = 2048
    config_data['maxAuthorizedExecutionTimeout'] = 0
    assert properties_validation(config_data)


def test_minimal_config():
    cd = {
        "supportedTransferProtocols": ["https"],
        "supportedModules": ["AdvancedData"],
        "supportedAPIVersion": "0.3"
    }
    assert properties_validation(cd)


def test_https_support(config_data):
    config_data['supportedTransferProtocols'] = ["http"]
    with pytest.raises(MissingRequiredParameterError):
        properties_validation(config_data)
