import enum
from typing import Dict, List
from marshmallow import Schema, fields, post_load, post_dump, validates, ValidationError
from marshmallow_enum import EnumField


class ExecutionStatus(enum.Enum):
    Initializing = "Initializing"
    Ready = "Ready"
    Running = "Running"
    Finished = "Finished"
    InitializationFailed = "InitializationFailed"
    ExecutionFailed = "ExecutionFailed"
    Unknown = "Unknown"
    Killed = "Killed"


EXECUTION_COMPLETED_STATUSES = [
    ExecutionStatus.Finished, ExecutionStatus.ExecutionFailed,
    ExecutionStatus.Unknown, ExecutionStatus.Killed
]


class ExecutionSchema(Schema):
    SKIP_VALUES = list([None])

    class Meta:
        ordered = True

    identifier = fields.Str()
    name = fields.Str(required=True)
    pipeline_identifier = fields.Str(
        required=True,
        dump_to='pipelineIdentifier',
        load_from='pipelineIdentifier')
    timeout = fields.Int()
    status = EnumField(ExecutionStatus)
    input_values = fields.Dict(
        required=True, dump_to='inputValues', load_from='inputValues')
    returned_files = fields.Dict(
        keys=fields.Str(),
        values=fields.List(fields.Url()),
        dump_to='returnedFiles',
        load_from='returnedFiles')
    study_identifier = fields.Str(
        dump_to='studyIdentifier', load_from='studyIdentifier')
    error_code = fields.Int(dump_to='errorCode', load_from='errorCode')
    start_date = fields.Int(dump_to='startDate', load_from='startDate')
    end_date = fields.Int(dump_to='endDate', load_from='endDate')

    @post_load
    def to_model(self, data):
        return Execution(**data)

    @post_dump
    def remove_skip_values(self, data):
        """remove_skip_values removes all values specified in the
        SKIP_VALUES set from appearing in the 'dumped' JSON.
        """
        return {
            key: value
            for key, value in data.items() if value not in self.SKIP_VALUES
        }


class Execution():
    schema = ExecutionSchema()

    def __init__(self,
                 name: str = None,
                 pipeline_identifier: str = None,
                 input_values: object = None,
                 identifier: str = None,
                 timeout: int = None,
                 status: ExecutionStatus = None,
                 returned_files: Dict[str, List[str]] = None,
                 study_identifier: str = None,
                 error_code: int = None,
                 start_date: int = None,
                 end_date: int = None):

        self.identifier = identifier
        self.name = name
        self.pipeline_identifier = pipeline_identifier
        self.timeout = timeout
        self.status = status
        self.input_values = input_values
        self.returned_files = returned_files
        self.study_identifier = study_identifier
        self.error_code = error_code
        self.start_date = start_date
        self.end_date = end_date
