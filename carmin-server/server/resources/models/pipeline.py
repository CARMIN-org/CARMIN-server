from typing import List

from .base_model import Model
from .error_code_and_message import ErrorCodeAndMessage
from .pipeline_parameter import PipelineParameter
from server.common import util


class Pipeline(Model):
    def __init__(self,
                 identifier: str = None,
                 name: str = None,
                 version: str = None,
                 description: str = None,
                 can_execute: bool = None,
                 parameters: List[PipelineParameter] = None,
                 error_codes_and_messages: List[ErrorCodeAndMessage] = None):
        """Pipeline - a model defined in Swagger

        Args:
            identifier (str): The identifier for this Pipeline.
            name (str): The name of this Pipeline.
            version (str): The version of this Pipeline.
            description (str): The description of this Pipeline.
            can_execute (bool): Indication of whether the Pipeline can execute.
            parameters (List[PipelineParameter]): The parameters of this Pipeline.
            
            #TODO: Implement the properties attribute. Need additional information on the actual representation.
            properties (string): 
            
            error_codes_and_messages (List[ErrorCodeAndMessage]): Error codes and messages for this Pipeline
        """
        self.swagger_types = {
            'identifier': str,
            'name': str,
            'version': str,
            'description': str,
            'can_execute': bool,
            'parameters': List[PipelineParameter],
            'error_codes_and_messages': List[ErrorCodeAndMessage]
        }

        self.attribute_map = {
            'identifier': 'identifier',
            'name': 'name',
            'version': 'version',
            'description': 'description',
            'can_execute': 'canExecute',
            'parameters': 'parameters',
            'error_codes_and_messages': 'errorCodesAndMessages'
        }

        self._identifier = identifier
        self._name = name
        self._version = version
        self._description = description
        self._can_execute = can_execute
        self._parameters = parameters
        self._error_codes_and_messages = error_codes_and_messages

    @classmethod
    def from_dict(cls, dikt) -> 'Pipeline':
        """Returns the Pipeline object from a dict.

        Args:
            dikt (Dict): A dict.
        Returns:
            Pipeline: A Pipeline object from the dict.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def identifier(self) -> str:
        """Gets the identifier of this Pipeline.

        Returns:
            str: The identifier of this Pipeline.
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        """Sets the identifier of this Pipeline.

        Args:
            identifier (str): The identifier of this Pipeline.
        Raises:
            ValueError: `identifier` must not be `None`.
        """
        if identifier is None:
            raise ValueError(
                "Invalid value for `identifier`, must not be `None`")

        self._identifier = identifier

    @property
    def name(self) -> str:
        """Gets the name of this Pipeline.

        Returns:
            str: The name of this Pipeline.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Pipeline.

        Args:
            name (str): The name of this Pipeline.
        Raises:
            ValueError: `name` must not be `None`.
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def version(self) -> str:
        """Gets the version of this Pipeline.

        Returns:
            str: The version of this Pipeline.
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this Pipeline.

        Args:
            version (str): The version of this Pipeline.
        Raises:
            ValueError: `version` must not be `None`.
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")

        self._version = version

    @property
    def description(self) -> str:
        """Gets the description of this Pipeline.

        Returns:
            str: The description of this Pipeline.
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Pipeline.

        Args:
            description (str): The description of this Pipeline.
        """

        self._description = description

    @property
    def can_execute(self) -> bool:
        """Gets the can_execute of this Pipeline.

        Returns:
            bool: True if this user who requested this Pipeline can execute it.
        """
        return self._can_execute

    @can_execute.setter
    def can_execute(self, can_execute: bool):
        """Sets the can_execute of this Pipeline.

        Args:
            can_execute (bool): True if the user who requested this Pipeline can execute it.
        """

        self._can_execute = can_execute

    @property
    def parameters(self) -> List[PipelineParameter]:
        """Gets the parameters of this Pipeline.

        Returns:
            List[PipelineParameter]: The parameters of this Pipeline.
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: List[PipelineParameter]):
        """Sets the parameters of this Pipeline.


        Args:
            parameters (List[PipelineParameter]): The parameters of this Pipeline.
        """

        self._parameters = parameters

    @property
    def error_codes_and_messages(self) -> List[ErrorCodeAndMessage]:
        """Gets the error_codes_and_messages of this Pipeline.


        Returns:
            List[ErrorCodeAndMessage]: The Errors related to this Pipeline.
        """
        return self._error_codes_and_messages

    @error_codes_and_messages.setter
    def error_codes_and_messages(
            self, error_codes_and_messages: List[ErrorCodeAndMessage]):
        """Sets the error_codes_and_messages of this Pipeline.


        Args:
            error_code_and_messages (List[ErrorCodeAndMessage]): The Errors related to this Pipeline.
        """

        self._error_codes_and_messages = error_codes_and_messages
