from .base_model import Model
from server.common.models.parameter_type import ParameterType
from server.common import util


class PipelineParameter(Model):
    def __init__(self,
                 name: str = None,
                 parameter_type: ParameterType = None,
                 is_optional: bool = None,
                 is_returned_value: bool = None,
                 default_value: object = None,
                 description: str = None):
        """PipelineParameter - a model defined in Swagger

        Args:
            name (str): The name of this PipelineParameter.
            parameter_type (ParameterType): The ParameterType of this PipelineParameter.
            is_optional (bool): Whether this PipelineParameter is optional.
            is_returned_value (bool): The is_returned_value of PipelineParameter.
            default_value (object): Default value. It must be consistent with the ParameterType.
            description (str): The description of this PipelineParameter.
        """
        self.swagger_types = {
            'name': str,
            'parameter_type': ParameterType,
            'is_optional': bool,
            'is_returned_value': bool,
            'default_value': object,
            'description': str
        }

        self.attribute_map = {
            'name': 'name',
            'parameter_type': 'type',
            'is_optional': 'isOptional',
            'is_returned_value': 'isReturnedValue',
            'default_value': 'defaultValue',
            'description': 'description'
        }

        self._name = name
        self._type = parameter_type
        self._is_optional = is_optional
        self._is_returned_value = is_returned_value
        self._default_value = default_value
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'PipelineParameter':
        """Returns the dict as a model.

        Args:
            dikt: A dict.
        Returns:
            PipelineParameter: The model generated from this dict.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this PipelineParameter.

        Returns:
            str: The name of this PipelineParameter.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this PipelineParameter.


        Args:
            name (str): The name of this PipelineParameter.
        Raises:
            ValueError: `name` must not be `None`.
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def type(self) -> ParameterType:
        """Gets the type of this PipelineParameter.

        Returns:
            ParameterType: The type of this PipelineParameter.
        """
        return self._type

    @type.setter
    def type(self, type: ParameterType):
        """Sets the type of this PipelineParameter.

        Args:
            type (ParameterType): The type of this PipelineParameter.
        Raises:
            ValueError: `type` must not be `None`.
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def is_optional(self) -> bool:
        """Gets the is_optional of this PipelineParameter.

        Returns:
            bool: True if PipelineParameter is optional.
        """
        return self._is_optional

    @is_optional.setter
    def is_optional(self, is_optional: bool):
        """Sets the is_optional of this PipelineParameter.

        Args:
            is_optional (bool): True if the PipelineParameter is optional.
        Raises:
            ValueError:  `is_optional` must not be `None`.
        """
        if is_optional is None:
            raise ValueError(
                "Invalid value for `is_optional`, must not be `None`")

        self._is_optional = is_optional

    @property
    def is_returned_value(self) -> bool:
        """Gets the is_returned_value of this PipelineParameter.

        Returns:
            (bool): The is_returned_value of this PipelineParameter.
        """
        return self._is_returned_value

    @is_returned_value.setter
    def is_returned_value(self, is_returned_value: bool):
        """Sets the is_returned_value of this PipelineParameter.

        Args:
            is_returned_value (bool): This is_returned_value of this PipelineParameter.
        Raises:
            ValueError: `is_returned_value` must not be `None`.
        """
        if is_returned_value is None:
            raise ValueError(
                "Invalid value for `is_returned_value`, must not be `None`")

        self._is_returned_value = is_returned_value

    @property
    def default_value(self) -> object:
        """Gets the default_value for this PipelineParameter.

        Returns:
            (object): The default value for this PipelineParameter.
        """

    @default_value.setter
    def default_value(self, default_value: object):
        """Sets the default_value for this PipelineParameter.

        Args:
            default_value (object): The default value. It must be consistent
            with the parameter type.
        """
        self._default_value = default_value

    @property
    def description(self) -> str:
        """Gets the description of this PipelineParameter.

        Returns:
            str: The description of this PipelineParameter.
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this PipelineParameter.

        Args:
            description (str): The description of this PipelineParameter.
        """

        self._description = description
