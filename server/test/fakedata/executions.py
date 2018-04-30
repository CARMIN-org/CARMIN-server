from server.resources.models.execution import Execution
from server.database.models.execution import Execution as ExecutionDB, ExecutionStatus
from server.test.fakedata.users import standard_user


def execution_for_db(execution_id: str, username: str) -> ExecutionDB:
    return ExecutionDB(
        identifier=execution_id,
        name="valid_execution",
        pipeline_identifier="pipeline1",
        status=ExecutionStatus.Finished,
        creator_username=username)


def post_valid_execution(pipeline_identifier: str):
    return Execution(
        name="valid_execution",
        pipeline_identifier=pipeline_identifier,
        input_values={
            "input_file":
            "http://localhost/path/{}/test.txt".format(
                standard_user().username)
        })


def post_invalid_execution_file_not_exist(pipeline_identifier: str):
    return Execution(
        name="invalid_execution",
        pipeline_identifier=pipeline_identifier,
        input_values={
            "input_file":
            "http://localhost/path/{}/does_not_exist.txt".format(
                standard_user().username)
        })


def post_invalid_execution_array_file_not_exist(pipeline_identifier: str):
    return Execution(
        name="invalid_execution",
        pipeline_identifier=pipeline_identifier,
        input_values={
            "input_file": [
                "http://localhost/path/{}/does_not_exist.txt".format(
                    standard_user().username),
                "http://localhost/path/{}/test.txt".format(
                    standard_user().username)
            ]
        })


POST_INVALID_EXECUTION_IDENTIFIER_NOT_EXIST = Execution(
    name="invalid_execution",
    pipeline_identifier="not_exist",
    input_values={
        "first": "value"
    })


def post_invalid_identifier_set(pipeline_identifier: str):
    return Execution(
        name="invalid_execution",
        pipeline_identifier=pipeline_identifier,
        identifier="an_invalid_identifier",
        input_values={
            "first": "value"
        })


POST_INVALID_MODEL = {"name": "invalid_execution"}

PATCH_VALID_EXECUTION = {"name": "new_name", "timeout": 1024}

PATCH_VALID_EXECUTION2 = {"name": "new_name"}

PATCH_VALID_EXECUTION3 = {"timeout": 1024}

PATCH_ILLEGAL_PARAMETER = {"status": "Finished"}
PATCH_ILLEGAL_PARAMETER2 = {"identifier": "my_custom_identifier"}

PATCH_INVALID_PARAMETER = {"timeout": "non_integer_timeout"}

PATCH_NO_CHANGE_PARAMETER = {"pipelineIdentifier": "new_pipeline_identifier"}
