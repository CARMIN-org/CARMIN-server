from typing import List

from server.common import util
from .base_model import Model
from .error_code_and_message import ErrorCodeAndMessage  # noqa: F401,E501


class PlatformProperties(Model):
    """PlatformProperties

    Attributes:
        platform_name (str): The platform_name of this PlatformProperties.
        api_error_codes_and_messages (List[ErrorCodeAndMessage]): The api_error_codes_and_messages of this PlatformProperties.
        supported_transfer_protocols (List[str]): The supported_transfer_protocols of this PlatformProperties.
        supported_modules (List[str]): The supported_modules of this PlatformProperties.
        default_limit_list_executions (int): The default_limit_list_executions of this PlatformProperties.
        email (str): The email of this PlatformProperties.
        platform_description (str): The platform_description of this PlatformProperties.
        min_authorized_execution_timeout (int): The min_authorized_execution_timeout of this PlatformProperties.
        max_authorized_execution_timeout (int): The max_authorized_execution_timeout of this PlatformProperties.
        default_execution_timeout (int): The default_execution_timeout of this PlatformProperties.
        unsupported_methods (List[str]): The unsupported_methods of this PlatformProperties.
        default_study (str): The default_study of this PlatformProperties.
        supported_api_version (str): The supported_api_version of this PlatformProperties.
        supported_pipeline_properties (List[str]): Complete list of all properties that can be used to describe the pipelines and to filter them in the "listPipelines" method        
    """

    def __init__(
            self,
            platform_name: str = None,
            api_error_codes_and_messages: List[ErrorCodeAndMessage] = None,
            supported_transfer_protocols: List[str] = None,
            supported_modules: List[str] = None,
            default_limit_list_executions: int = None,
            email: str = None,
            platform_description: str = None,
            min_authorized_execution_timeout: int = None,
            max_authorized_execution_timeout: int = None,
            default_execution_timeout: int = None,
            unsupported_methods: List[str] = None,
            default_study: str = None,
            supported_api_version: str = None,
            supported_pipeline_properties: List[str] = None):

        self.swagger_types = {
            'platform_name': str,
            'api_error_codes_and_messages': List[ErrorCodeAndMessage],
            'supported_transfer_protocols': List[str],
            'supported_modules': List[str],
            'default_limit_list_executions': int,
            'email': str,
            'platform_description': str,
            'min_authorized_execution_timeout': int,
            'max_authorized_execution_timeout': int,
            'default_execution_timeout': int,
            'unsupported_methods': List[str],
            'default_study': str,
            'supported_api_version': str,
            'supported_pipeline_properties': List[str]
        }

        self.attribute_map = {
            'platform_name': 'platformName',
            'api_error_codes_and_messages': 'APIErrorCodesAndMessages',
            'supported_transfer_protocols': 'supportedTransferProtocols',
            'supported_modules': 'supportedModules',
            'default_limit_list_executions': 'defaultLimitListExecutions',
            'email': 'email',
            'platform_description': 'platformDescription',
            'min_authorized_execution_timeout':
            'minAuthorizedExecutionTimeout',
            'max_authorized_execution_timeout':
            'maxAuthorizedExecutionTimeout',
            'default_execution_timeout': 'defaultExecutionTimeout',
            'unsupported_methods': 'unsupportedMethods',
            'default_study': 'defaultStudy',
            'supported_api_version': 'supportedAPIVersion',
            'supported_pipeline_properties': 'supportedPipelineProperties'
        }

        self._platform_name = platform_name
        self._api_error_codes_and_messages = api_error_codes_and_messages
        self._supported_transfer_protocols = supported_transfer_protocols
        self._supported_modules = supported_modules
        self._default_limit_list_executions = default_limit_list_executions
        self._email = email
        self._platform_description = platform_description
        self._min_authorized_execution_timeout = min_authorized_execution_timeout
        self._max_authorized_execution_timeout = max_authorized_execution_timeout
        self._default_execution_timeout = default_execution_timeout
        self._unsupported_methods = unsupported_methods
        self._default_study = default_study
        self._supported_api_version = supported_api_version
        self._supported_pipeline_properties = supported_pipeline_properties

    @classmethod
    def from_dict(cls, dikt) -> 'PlatformProperties':
        """Returns the dict as a model

        Args:
            dikt (dict): A dict.
        Returns:
           PlatformProperties: The PlatformProperties of this PlatformProperties.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def platform_name(self) -> str:
        """Gets the platform_name of this PlatformProperties.

        Returns:
            str: The platform_name of this PlatformProperties.
        """
        return self._platform_name

    @platform_name.setter
    def platform_name(self, platform_name: str):
        """Sets the platform_name of this PlatformProperties.

        Args:
            platform_name (str): The platform_name of this PlatformProperties.
        """

        self._platform_name = platform_name

    @property
    def api_error_codes_and_messages(self) -> List[ErrorCodeAndMessage]:
        """Gets the api_error_codes_and_messages of this PlatformProperties.

        Returns:
            List[ErrorCodeAndMessage]: The api_error_codes_and_messages of this PlatformProperties.
        """
        return self._api_error_codes_and_messages

    @api_error_codes_and_messages.setter
    def api_error_codes_and_messages(
            self, api_error_codes_and_messages: List[ErrorCodeAndMessage]):
        """Sets the api_error_codes_and_messages of this PlatformProperties.

        Args:
            api_error_codes_and_messages (List[ErrorCodeAndMessage]): The api_error_codes_and_messages of this PlatformProperties.
        """

        self._api_error_codes_and_messages = api_error_codes_and_messages

    @property
    def supported_transfer_protocols(self) -> List[str]:
        """Gets the supported_transfer_protocols of this PlatformProperties.

        Protocol names must be URL prefixes (e.g. \"http\", \"https\", \"ftp\", \"sftp\", \"ftps\", \"scp\", \"webdav\").

        Returns:
            List[str]: The supported_transfer_protocols of this PlatformProperties.
        """
        return self._supported_transfer_protocols

    @supported_transfer_protocols.setter
    def supported_transfer_protocols(self,
                                     supported_transfer_protocols: List[str]):
        """Sets the supported_transfer_protocols of this PlatformProperties.

        Protocol names must be URL prefixes (e.g. \"http\", \"https\", \"ftp\", \"sftp\", \"ftps\", \"scp\", \"webdav\").

        Args:
            supported_transfer_protocols (List[str]): The supported_transfer_protocols
            of this PlatformProperties.
        """
        allowed_values = [
            "http", "https", "ftp", "sftp", "ftps", "scp", "webdav"
        ]
        if not set(supported_transfer_protocols).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `supported_transfer_protocols` [{0}], must be a subset of [{1}]"
                .format(", ".join(
                    map(str,
                        set(supported_transfer_protocols) -
                        set(allowed_values))), ", ".join(
                            map(str, allowed_values))))

        self._supported_transfer_protocols = supported_transfer_protocols

    @property
    def supported_modules(self) -> List[str]:
        """Gets the supported_modules of this PlatformProperties.


        Returns:
            List[str]: The supported_modules of this PlatformProperties.
        """
        return self._supported_modules

    @supported_modules.setter
    def supported_modules(self, supported_modules: List[str]):
        """Sets the supported_modules of this PlatformProperties.

        Args:
            supported_modules (List[str]): The supported_modules of this PlatformProperties.
        """
        allowed_values = ["Processing", "Data", "Management", "Commercial"]
        if not set(supported_modules).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `supported_modules` [{0}], must be a subset of [{1}]"
                .format(", ".join(
                    map(str,
                        set(supported_modules) - set(allowed_values))),
                        ", ".join(map(str, allowed_values))))

        self._supported_modules = supported_modules

    @property
    def default_limit_list_executions(self) -> int:
        """Gets the default_limit_list_executions of this PlatformProperties.

        The number of Executions returned by getExecutions

        Returns:
            int: The default_limit_list_executions of this PlatformProperties.
        """
        return self._default_limit_list_executions

    @default_limit_list_executions.setter
    def default_limit_list_executions(self,
                                      default_limit_list_executions: int):
        """Sets the default_limit_list_executions of this PlatformProperties.

        The number of Executions returned by getExecutions

        Args:
            default_limit_list_executions (int): The default_limit_list_executions
            of this PlatformProperties.
        """

        self._default_limit_list_executions = default_limit_list_executions

    @property
    def email(self) -> str:
        """Gets the email of this PlatformProperties.


        Returns:
            str: The email of this PlatformProperties.
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this PlatformProperties.

        Args:
            email (str): The email of this PlatformProperties.
        """

        self._email = email

    @property
    def platform_description(self) -> str:
        """Gets the platform_description of this PlatformProperties.

        Returns:
            str: The platform_description of this PlatformProperties.
        """
        return self._platform_description

    @platform_description.setter
    def platform_description(self, platform_description: str):
        """Sets the platform_description of this PlatformProperties.

        Args:
            platform_description (str): The platform_description of this PlatformProperties.
        """

        self._platform_description = platform_description

    @property
    def min_authorized_execution_timeout(self) -> int:
        """Gets the min_authorized_execution_timeout of this PlatformProperties.


        Returns:
            int: The min_authorized_execution_timeout of this PlatformProperties.
        """
        return self._min_authorized_execution_timeout

    @min_authorized_execution_timeout.setter
    def min_authorized_execution_timeout(
            self, min_authorized_execution_timeout: int):
        """Sets the min_authorized_execution_timeout of this PlatformProperties.

        Args:
            min_authorized_execution_timeout (int): The min_authorized_execution_timeout
            of this PlatformProperties.
        """

        self._min_authorized_execution_timeout = min_authorized_execution_timeout

    @property
    def max_authorized_execution_timeout(self) -> int:
        """Gets the max_authorized_execution_timeout of this PlatformProperties.

        0 or absent means no max timeout. max has to be greater or equal to the min.

        Returns:
            int: The max_authorized_execution_timeout of this PlatformProperties.
        """
        return self._max_authorized_execution_timeout

    @max_authorized_execution_timeout.setter
    def max_authorized_execution_timeout(
            self, max_authorized_execution_timeout: int):
        """Sets the max_authorized_execution_timeout of this PlatformProperties.

        0 or absent means no max timeout. max has to be greater or equal to the min.

        Args:
            max_authorized_execution_timeout (int): The max_authorized_execution_timeout
        of this PlatformProperties.
        """
        self._max_authorized_execution_timeout = max_authorized_execution_timeout

    @property
    def default_execution_timeout(self) -> int:
        """Gets the default_execution_timeout of this PlatformProperties.


        Returns:
            int: The default_execution_timeout of this PlatformProperties.
        """
        return self._default_execution_timeout

    @default_execution_timeout.setter
    def default_execution_timeout(self, default_execution_timeout: int):
        """Sets the default_execution_timeout of this PlatformProperties.


        Args:
            default_execution_timeout (int): The default_execution_timeout of
            this PlatformProperties.
        """
        self._default_execution_timeout = default_execution_timeout

    @property
    def unsupported_methods(self) -> List[str]:
        """Gets the unsupported_methods of this PlatformProperties.

        List of optional methods that are not supported by the platform. Must be
        consistent with the \"isKillExecutionSupported\" property.

        Returns:
            List[str]: The unsupported_methods of this PlatformProperties.
        """
        return self._unsupported_methods

    @unsupported_methods.setter
    def unsupported_methods(self, unsupported_methods: List[str]):
        """Sets the unsupported_methods of this PlatformProperties.

        List of optional methods that are not supported by the platform. Must be
        consistent with the \"isKillExecutionSupported\" property.

        Args:
            unsupported_methods (List[str]): The unsupported_methods of this PlatformProperties.
        """
        self._unsupported_methods = unsupported_methods

    @property
    def default_study(self) -> str:
        """Gets the default_study of this PlatformProperties.

        Returns
            str: The default_study of this PlatformProperties.
        """
        return self._default_study

    @default_study.setter
    def default_study(self, default_study: str):
        """Sets the default_study of this PlatformProperties.

        Args:
            default_study (str): The default_study of this PlatformProperties.
        """

        self._default_study = default_study

    @property
    def supported_api_version(self) -> str:
        """Gets the supported_api_version of this PlatformProperties.

        Returns:
            str: The supported_api_version of this PlatformProperties.
        """
        return self._supported_api_version

    @supported_api_version.setter
    def supported_api_version(self, supported_api_version: str):
        """Sets the supported_api_version of this PlatformProperties.

        Args:
            supported_api_version (str): The supported_api_version of this PlatformProperties.
        """
        if supported_api_version is None:
            raise ValueError(
                "Invalid value for `supported_api_version`, must not be `None`"
            )

        self._supported_api_version = supported_api_version

    @property
    def supported_pipeline_properties(self) -> List[str]:
        """Gets the supported_pipeline_properties of this PlatformProperties.

        Returns:
            List[str]: The supported_pipeline_properties of this PlatformProperties.
        """
        return self._supported_pipeline_properties

    @supported_pipeline_properties.setter
    def supported_pipeline_properties(
            self, supported_pipeline_properties: List[str]):
        """Sets the supported_pipeline_properties of this PlatformProperties.

        Args:
            supported_pipeline_properties (List[str]): The supported_pipeline_properties
            of this PlatformProperties.
        """
        if supported_pipeline_properties is None:
            raise ValueError(
                "Invalid value for `supported_pipeline_properties`, must not be `None`"
            )

        self._supported_pipeline_properties = supported_pipeline_properties
