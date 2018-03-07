from server.resources.models.execution import Execution
from server.test.fakedata.users import standard_user

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
            "http://localhost/path/{}/test.txt".format(
                standard_user().username),
            "http://localhost/path/{}/does_not_exist.txt".format(
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
