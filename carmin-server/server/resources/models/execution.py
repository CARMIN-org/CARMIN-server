from typing import List, Dict
from .base_model import Model
from server.common import util


#TODO: Redo from code-gen
class Execution(Model):
    """A Pipeline Execution

    Attributes:
        identifier (str, optional readonly):
        name (str):
        pipeline_identifier (str):
        timeout (int, optional):
        status (str, optional readonly):
        input_values (object):
        returned_files (Dict[str, List[str]]):
        study_identifier (str):
        error_code (int):
        start_date (int):
        end_date (int):
    """

    def __init__(self,
                 identifier: str = None,
                 name: str = None,
                 pipeline_identifier: str = None,
                 timeout: int = None,
                 status: str = None,
                 input_values: object = None,
                 returned_files: Dict[str, List[str]] = None,
                 study_identifier: str = None,
                 error_code: int = None,
                 start_date: int = None,
                 end_date: int = None):
        self.swagger_types = {
            'identifier': str,
            'name': str,
            'pipeline_identifier': str,
            'timeout': int,
            'status': str,
            'input_values': object,
            'returned_files': Dict[str, List[str]],
            'study_identifier': str,
            'error_code': int,
            'start_date': int,
            'end_date': int
        }

        self.attribute_map = {
            'identifier': 'identifier',
            'name': 'name',
            'pipeline_identifier': 'pipelineIdentifier',
            'timeout': 'timeout',
            'status': 'status',
            'input_values': 'inputValues',
            'returned_files': 'returnedFiles',
            'study_identifier': 'studyIdentifier',
            'error_code': 'errorCode',
            'start_date': 'startDate',
            'end_date': 'endDate'
        }

        self._identifier = identifier
        self._name = name
        self._pipeline_identifier = pipeline_identifier
        self._timeout = timeout
        self._status = status
        self._input_values = input_values
        self._returned_files = returned_files
        self._study_identifier = study_identifier
        self._error_code = error_code
        self._start_date = start_date
        self._end_date = end_date
