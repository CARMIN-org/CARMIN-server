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


POST_VALID_EXECUTION = Execution(
    name="valid_execution",
    pipeline_identifier="pipeline1",
    input_values={
        "file_input":
        "http://localhost/path/{}/test.txt".format(standard_user().username)
    })

POST_INVALID_EXECUTION_FILE_NOT_EXIST = Execution(
    name="invalid_execution",
    pipeline_identifier="pipeline1",
    input_values={
        "file_input":
        "http://localhost/path/{}/does_not_exist.txt".format(
            standard_user().username)
    })

POST_INVALID_EXECUTION_ARRAY_FILE_NOT_EXIST = Execution(
    name="invalid_execution",
    pipeline_identifier="pipeline1",
    input_values={
        "file_input": [
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

POST_INVALID_IDENTIFIER_SET = Execution(
    name="invalid_execution",
    pipeline_identifier="pipeline1",
    identifier="an_identifier",
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
